from astropy.io import fits
import h5py
import os
from astropy.wcs import WCS
from tqdm import tqdm
import numpy as np
import keras
import pyregion
import time
from joblib import Parallel, delayed
from LuciFit import Fit
import matplotlib.pyplot as plt


class Luci():
    """
    This is the primary class for the general purpose line fitting code LUCI. This contains
    all io/administrative functionality. The fitting functionality can be found in the
    Fit class (Lucifit.py).
    """
    def __init__(self, cube_path, output_dir, object_name, redshift, ref_spec=None, model_ML_name=None):
        """
        Initialize our Luci class -- this acts similar to the SpectralCube class
        of astropy or spectral-cube.
        Args:
            cube_path: Full path to hdf5 cube with the hdf5 extension (e.x. '/user/home/M87.hdf5')
            output_dir: Full path to output directory
            object_name: Name of the object to fit. This is used for naming purposes. (e.x. 'M87')
            redshift: Redshift to the object. (e.x. 0.00428)
            ref_spec: Name of reference spectrum for machine learning algo (e.x. 'Reference-Spectrum-R5000')
            model_ML_name: Name of pretrained machine learning model
        """
        self.cube_path = cube_path
        self.output_dir = output_dir+'/Luci'
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        self.object_name = object_name
        self.redshift = redshift
        self.ref_spec = ref_spec+'.fits'
        if model_ML_name != None or '':
            self.model_ML = keras.models.load_model(model_ML_name)
        else:
            self.model_ML = model_ML_name
        self.quad_nb = 0  # Number of quadrants in Hdf5
        self.dimx = 0  # X dimension of cube
        self.dimy = 0  # Y dimension of cube
        self.dimz = 0  # Z dimension of cube
        self.cube_final = None  # Complete data cube
        self.cube_binned = None  # Binned data cube
        self.header = None
        self.deep_image = None
        self.spectrum_axis = None
        self.wavenumbers_syn = None
        self.hdr_dict = None
        self.read_in_cube()
        self.spectrum_axis_func()
        self.read_in_reference_spectrum()


    def get_quadrant_dims(self, quad_number):
        """
        Calculate the x and y limits of a given quadrant in the HDF5 file. The
        data cube is saved in 9 individual arrays in the original HDF5 cube. This
        function gets the bouunds for each quadrant.
        Args:
            quad_number: Quadrant Number
        Return:
            x_min, x_max, y_min, y_max: Spatial bounds of quadrant
        """
        div_nb = int(np.sqrt(self.quad_nb))
        if (quad_number < 0) or (quad_number > self.quad_nb - 1):
            raise StandardError("quad_number out of bounds [0," + str(self.quad_nb- 1) + "]")
            return "SOMETHING FAILED"

        index_x = quad_number % div_nb
        index_y = (quad_number - index_x) / div_nb

        x_min = index_x * np.floor(self.dimx / div_nb)
        if (index_x != div_nb - 1):
            x_max = (index_x  + 1) * np.floor(self.dimx / div_nb)
        else:
            x_max = self.dimx

        y_min = index_y * np.floor(self.dimy / div_nb)
        if (index_y != div_nb - 1):
            y_max = (index_y  + 1) * np.floor(self.dimy / div_nb)
        else:
            y_max = self.dimy
        return int(x_min), int(x_max), int(y_min), int(y_max)


    def update_header(self, file):
        """
        Create a standard WCS header from the HDF5 header
        Args:
            file: hdf5 File object containing HDF5 file
        """
        hdr_dict = {}
        header_cols = [str(val[0]).replace("'b",'').replace("'", "").replace("b",'') for val in list(file['header'][()])]
        header_vals = [str(val[1]).replace("'b",'').replace("'", "").replace("b",'') for val in list(file['header'][()])]
        header_types = [val[3] for val in list(file['header'][()])]
        for header_col, header_val, header_type in zip(header_cols,header_vals, header_types):
            if 'bool' in str(header_type):
                hdr_dict[header_col] = bool(header_val)
            if 'float' in str(header_type):
                hdr_dict[header_col] = float(header_val)
            if 'int' in str(header_type):
                hdr_dict[header_col] = int(header_val)
            #print(header_type)
            else:
                try:
                    hdr_dict[header_col] = float(header_val)
                except:
                    hdr_dict[header_col] = str(header_val)
        hdr_dict['CTYPE3'] = 'WAVE-SIP'
        hdr_dict['CUNIT3'] = 'm'
        # Make WCS
        wcs_data = WCS(hdr_dict, naxis=2)
        self.header = wcs_data.to_header()
        self.hdr_dict = hdr_dict


    def create_deep_image(self, output_name=None):
        """
        Create deep image fits file of the cube. This takes the cube and averages
        the spectral axis. Then the deep image is saved as a fits file with the following
        naming convention: output_dir+'/'+object_name+'_deep.fits'
        """
        hdu = fits.PrimaryHDU()
        self.deep_image = np.mean(self.cube_final, axis=2)
        if output_name == None:
            output_name = self.output_dir+'/'+self.object_name+'_deep.fits'
        fits.writeto(output_name, self.deep_image.T, self.header, overwrite=True)

    def read_in_cube(self):
        """
        Function to read the hdf5 data into a 3d numpy array (data cube). We also
        translate the header to standard wcs format by calling the update_header function.
        """
        print('Reading in data...')
        file =  h5py.File(self.cube_path+'.hdf5', 'r')  # Read in file
        self.quad_nb = file.attrs['quad_nb']  # Get the number of quadrants
        self.dimx = file.attrs['dimx']  # Get the dimensions in x
        self.dimy = file.attrs['dimy']  # Get the dimensions in y
        self.dimz = file.attrs['dimz']  # Get the dimensions in z (spectral axis)
        self.cube_final = np.zeros((self.dimx, self.dimy, self.dimz))  # Complete data cube
        for iquad in tqdm(range(self.quad_nb)):
            xmin,xmax,ymin,ymax = self.get_quadrant_dims(iquad)
            iquad_data = file['quad00%i'%iquad]['data'][:]  # Save data to intermediate array
            iquad_data[(np.isfinite(iquad_data) == False)]= 1e-22 # Modifs
            iquad_data[(iquad_data < -1e-16)]= -1e-22 # Modifs
            iquad_data[(iquad_data > 1e-9)]= 1e-22 # Modifs
            self.cube_final[xmin:xmax, ymin:ymax, :] = iquad_data  # Save to correct location in main cube
        self.update_header(file)

    def spectrum_axis_func(self):
        """
        Create the x-axis for the spectra. We must construct this from header information
        since each pixel only has amplitudes of the spectra at each point.
        """
        len_wl = self.cube_final.shape[2]  # Length of Spectral Axis
        start = self.hdr_dict['CRVAL3']  # Starting value of the spectral x-axis
        end = start + (len_wl)*self.hdr_dict['CDELT3']  # End
        #step = hdr_dict['CDELT3']  # Step size
        self.spectrum_axis = np.array(np.linspace(start, end, len_wl)*(self.redshift+1), dtype=np.float32)  # Apply redshift correction


    def read_in_reference_spectrum(self):
        """
        Read in the reference spectrum that will be used in the machine learning
        algorithm to interpolate the true spectra so that they
        wil all have the same size (required for our CNN). The reference spectrum
        will be saved as self.wavenumbers_syn [cm-1].
        """
        ref_spec = fits.open(self.ref_spec)[1].data
        channel = []
        counts = []
        for chan in ref_spec:  # Only want SN3 region
            channel.append(chan[0])
            counts.append(np.real(chan[1]))
        min_ = np.argmin(np.abs(np.array(channel)-14700))
        max_ = np.argmin(np.abs(np.array(channel)-15600))
        self.wavenumbers_syn = np.array(channel[min_:max_], dtype=np.float32)

    def fit_entire_cube(self, lines, fit_function):
        """
        Fit the entire cube (all spatial dimensions)
        Args:
            lines: Lines to fit (e.x. ['Halpha', 'NII6583'])
            fit_function: Fitting function to use (e.x. 'gaussian')
        """
        x_min = 0
        x_max = self.cube_final.shape[0]
        y_min = 0
        y_max = self.cube_final.shape[1]
        self.fit_cube(lines, fit_function, x_min, x_max, y_min, y_max)


    def bin_cube(self, binning, x_min, x_max, y_min, y_max):
        """
        Function to bin cube into bin x bin sub cubes
        Args:
            binning: Size of binning (equal in x and y direction)
        Return:
            Binned cubed called self.cube_binned and new spatial limits
        """
        x_shape_new = int((x_max-x_min)/binning)
        y_shape_new = int((y_max-y_min)/binning)
        binned_cube = np.zeros((x_shape_new, y_shape_new, self.cube_final.shape[2]))
        for i in range(x_shape_new):
            for j in range(y_shape_new):
                summed_spec = self.cube_final[x_min+int(i*binning):x_min+int((i+1)*binning), y_min+int(j*binning):y_min+int((j+1)*binning), :]
                #print(summed_spec[-1])
                summed_spec = np.nansum(summed_spec, axis=0)
                #print(summed_spec[-1])
                summed_spec = np.nansum(summed_spec, axis=0)
                #print(summed_spec)
                binned_cube[i,j] = summed_spec[:]
        self.header_binned = self.header
        self.header_binned['CRVAL1'] = self.header_binned['CRVAL1']/binning
        self.header_binned['CRVAL2'] = self.header_binned['CRVAL2']/binning
        self.header_binned['CDELT1'] = self.header_binned['CDELT1']/binning
        self.header_binned['CDELT2'] = self.header_binned['CDELT2']/binning
        #print(binned_cube.shape)
        self.cube_binned = binned_cube / (binning**2)
        #return binned_cube / (binning**2)


    def save_fits(self, lines, velocity_fits, broadening_fits, ampls_fits, flux_fits, chi2_fits, header, output_name, binning):
        if binning is not None:
            output_name = output_name + "_" + str(binning)
        fits.writeto(output_name+'_velocity.fits', velocity_fits.T, header, overwrite=True)
        fits.writeto(output_name+'_broadening.fits', broadening_fits.T, header, overwrite=True)
        for ct,line_ in enumerate(lines):  # Step through each line to save their individual amplitudes
            fits.writeto(output_name+'_'+line_+'_Amplitude.fits', ampls_fits[:,:,ct].T, header, overwrite=True)
            fits.writeto(output_name+'_'+line_+'_Flux.fits', flux_fits[:,:,ct].T, header, overwrite=True)
        fits.writeto(output_name+'_Chi2.fits', chi2_fits.T, header, overwrite=True)


    def fit_cube(self, lines, fit_function, x_min, x_max, y_min, y_max, bkg=None, binning=None, bayes_bool=False, output_name=None):
        """
        Primary fit call to fit rectangular regions in the data cube. This wraps the
        LuciFits.FIT().fit() call which applies all the fitting steps. This also
        saves the velocity and broadening fits files.
        Args:
            lines: Lines to fit (e.x. ['Halpha', 'NII6583'])
            fit_function: Fitting function to use (e.x. 'gaussian')
            x_min: Lower bound in x
            x_max: Upper bound in x
            y_min: Lower bound in y
            y_max: Upper bound in y
            bkg: Background Spectrum (1D numpy array; default None)
            binning:  Value by which to bin (default None)
            bayes_bool: Boolean to determine whether or not to run Bayesian analysis (default None)
            output_name: User defined output path/name (default None)
        Return:
            Velocity and Broadening arrays (2d). Also return amplitudes array (3D).
        """
        # Initialize fit solution arrays
        if binning != None:
            self.bin_cube(binning, x_min, x_max, y_min, y_max)
            #x_min = int(x_min/binning) ; y_min = int(y_min/binning) ; x_max = int(x_max/binning) ;  y_max = int(y_max/binning)
            x_max = int((x_max-x_min)/binning) ;  y_max = int((y_max-y_min)/binning)
            x_min = 0 ; y_min = 0
        velocity_fits = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        broadening_fits = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        chi2_fits = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        # First two dimensions are the X and Y dimensions.
        #The third dimension corresponds to the line in the order of the lines input parameter.
        ampls_fits = np.zeros((x_max-x_min, y_max-y_min, len(lines)), dtype=np.float32)
        flux_fits = np.zeros((x_max-x_min, y_max-y_min, len(lines)), dtype=np.float32)
        if output_name == None:
            output_name = self.output_dir+'/'+self.object_name
        for i in tqdm(range(x_max-x_min)):
            x_pix = x_min + i
            vel_local = []
            broad_local = []
            ampls_local = []
            flux_local = []
            chi2_local = []
            for j in range(y_max-y_min):
                y_pix = y_min+j
                if binning is not None:
                    sky = self.cube_binned[y_pix, x_pix, :]
                else:
                    sky = self.cube_final[y_pix, x_pix, :]
                if bkg is not None:
                    sky -= bkg  # Subtract background spectrum
                good_sky_inds = [~np.isnan(sky)]  # Clean up spectrum
                sky = sky[good_sky_inds]
                axis = self.spectrum_axis[good_sky_inds]
                # Call fit!
                fit = Fit(sky, axis, self.wavenumbers_syn, fit_function, lines,
                        self.model_ML, Plot_bool = False, bayes_bool=bayes_bool)
                fit_dict = fit.fit()
                # Save local list of fit values
                vel_local.append(fit_dict['velocity'])
                broad_local.append(fit_dict['broadening'])
                ampls_local.append(fit_dict['amplitudes'])
                flux_local.append(fit_dict['fluxes'])
                chi2_local.append(fit_dict['chi2'])
            # Update global array of fit values
            velocity_fits[i] = vel_local
            broadening_fits[i] = broad_local
            ampls_fits[i] = ampls_local
            flux_fits[i] = flux_local
            chi2_fits[i] = chi2_local
        # Write outputs (Velocity, Broadening, and Amplitudes)
        if binning is not None:
            self.save_fits(lines, velocity_fits, broadening_fits, ampls_fits, flux_fits, chi2_fits, self.header, output_name, binning)
            fits.writeto(output_name+'_velocity.fits', velocity_fits.T,  self.header, overwrite=True)
        else:
            self.save_fits(lines, velocity_fits, broadening_fits, ampls_fits, flux_fits, chi2_fits, self.header, output_name, binning)
        return velocity_fits, broadening_fits, flux_fits, chi2_fits

        #n_threads = 1
        #for i in range(x_max-x_min):
            #SNR_calc(VEL, BROAD, i)
        #Parallel(n_jobs=n_threads, backend="threading", batch_size=int((x_max-x_min)/n_threads))(delayed(SNR_calc)(VEL, BROAD, i) for i in range(x_max-x_min));
        #Parallel(n_jobs=n_threads, backend="threading")(delayed(SNR_calc)(VEL, BROAD, i) for i in tqdm(range(x_max-x_min)));

    def fit_region(self, lines, fit_function, region, bkg= None, bayes_bool=False, output_name=None):
        """
        Fit the spectrum in a region. This is an extremely similar command to fit_cube except
        it works for ds9 regions. We first create a mask from the ds9 region file. Then
        we step through the cube and only fit the unmasked pixels. Although this may not
        be the most efficient method, it does ensure the fidelity of the wcs system.
        Args:
            lines: Lines to fit (e.x. ['Halpha', 'NII6583'])
            fit_function: Fitting function to use (e.x. 'gaussian')
            region: Name of ds9 region file (e.x. 'region.reg'). You can also pass a boolean mask array.
            bkg: Background Spectrum (1D numpy array; default None)
            bayes_bool: Boolean to determine whether or not to run Bayesian analysis
            output_name: User defined output path/name
        Return:
            Velocity and Broadening arrays (2d). Also return amplitudes array (3D).
        """
        # Create mask
        if '.reg' in region:
            shape = (2048, 2064)#(self.header["NAXIS1"], self.header["NAXIS2"])  # Get the shape
            r = pyregion.open(region).as_imagecoord(self.header)  # Obtain pyregion region
            mask = r.get_mask(shape=shape)  # Calculate mask from pyregion region
        else:
            mask = np.load(region)
        # Set spatial bounds for entire cube
        x_min = 0
        x_max = self.cube_final.shape[0]
        y_min = 0
        y_max = self.cube_final.shape[1]
        # Initialize fit solution arrays
        velocity_fits = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        broadening_fits = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        if len(region.split('/')) > 1:  # If region file is a path, just keep the name for output purposes
            region = region.split('/')[-1]
        if output_name == None:
            output_name = self.output_dir+'/'+self.object_name+'_'+region.split('.')[0]
        # First two dimensions are the X and Y dimensions.
        #The third dimension corresponds to the line in the order of the lines input parameter.
        ampls_fits = np.zeros((x_max-x_min, y_max-y_min, len(lines)), dtype=np.float32)
        flux_fits = np.zeros((x_max-x_min, y_max-y_min, len(lines)), dtype=np.float32)
        for i in tqdm(range(x_max-x_min)):
            x_pix = x_min + i
            vel_local = []
            broad_local = []
            ampls_local = []
            flux_local = []
            for j in range(y_max-y_min):
                y_pix = y_min+j
                # Check if pixel is in the mask or not
                # If so, fit as normal. Else, set values to zero
                if mask[x_pix, y_pix] == True:
                    sky = self.cube_final[x_pix, y_pix, :]
                    if bkg is not None:
                        sky -= bkg
                    good_sky_inds = [~np.isnan(sky)]  # Clean up spectrum
                    sky = sky[good_sky_inds]
                    axis = self.spectrum_axis[good_sky_inds]
                    # Call fit!
                    fit = Fit(sky, axis, self.wavenumbers_syn, fit_function, lines,
                            self.model_ML, Plot_bool = False, bayes_bool=bayes_bool)
                    fit_dict = fit.fit()
                    # Save local list of fit values
                    vel_local.append(fit_dict['velocity'])
                    broad_local.append(fit_dict['broadening'])
                    ampls_local.append(fit_dict['amplitudes'])
                    flux_local.append(fit_dict['fluxes'])
                else:
                    vel_local.append(0)
                    broad_local.append(0)
                    ampls_local.append([0]*len(lines))
                    flux_local.append([0]*len(lines))
            # Update global array of fit values
            velocity_fits[i] = vel_local
            broadening_fits[i] = broad_local
            ampls_fits[i] = ampls_local
            flux_fits[i] = flux_local
            # Write outputs (Velocity, Broadening, and Amplitudes)
        fits.writeto(output_name+'_velocity.fits', velocity_fits.T, self.header, overwrite=True)
        fits.writeto(output_name+'_broadening.fits', broadening_fits.T, self.header, overwrite=True)
        for ct,line_ in enumerate(lines):  # Step through each line to save their individual amplitudes
            fits.writeto(output_name+line_+'_Amplitude.fits', ampls_fits[:,:,ct].T, self.header, overwrite=True)
            fits.writeto(output_name+line_+'_Flux.fits', flux_fits[:,:,ct].T, self.header, overwrite=True)

        return velocity_fits, broadening_fits, flux_fits


    def extract_spectrum_region(self, region, mean=False):
        """
        Extract spectrum in region. This is primarily used to extract background regions.
        The spectra in the region are summed and then averaged (if mean is selected).
        Using the 'mean' argument, we can either calculate the total summed spectrum (False)
        or the averaged spectrum for background spectra (True).
        Args:
            region: Name of ds9 region file (e.x. 'region.reg'). You can also pass a boolean mask array.
            mean: Boolean to determine whether or not the mean spectrum is taken. This is used for calculating background spectra.
        Return:
            X-axis and spectral axis of region.
        """
        # Create mask
        if '.reg' in region:
            shape = (2048, 2064)#(self.header["NAXIS1"], self.header["NAXIS2"])  # Get the shape
            r = pyregion.open(region).as_imagecoord(self.header)  # Obtain pyregion region
            mask = r.get_mask(shape=shape)  # Calculate mask from pyregion region
        else:
            mask = region
        # Set spatial bounds for entire cube
        x_min = 0
        x_max = self.cube_final.shape[0]
        y_min = 0
        y_max = self.cube_final.shape[1]
        integrated_spectrum = np.zeros(self.cube_final.shape[2])
        spec_ct = 0
        for i in tqdm(range(x_max-x_min)):
            x_pix = x_min + i
            for j in range(y_max-y_min):
                y_pix = y_min+j
                # Check if pixel is in the mask or not
                if mask[x_pix, y_pix] == True:
                    integrated_spectrum += self.cube_final[y_pix, x_pix, :]
                    spec_ct += 1
                else:
                    pass
        if mean == True:
            integrated_spectrum /= spec_ct
        return self.spectrum_axis, integrated_spectrum


    def create_snr_map(self, x_min=0, x_max=2048, y_min=0, y_max=2064, method=1):
        """
        Create signal-to-noise ratio (SNR) map of a given region. If no bounds are given,
        a map of the entire cube is calculated.
        Args:
            x_min: Minimal X value (default 0)
            x_max: Maximal X value (default 2048)
            y_min: Minimal Y value (default 0)
            y_max: Maximal Y value (default 2064)
            method: Method used to calculate SNR (default 1; options 1 or 2)
        Return:
            snr_map: Signal-to-Noise ratio map
        """
        # Calculate bounds for SNR calculation
        # Step through spectra
        SNR = np.zeros((x_max-x_min, y_max-y_min), dtype=np.float32)
        start = time.time()
        def SNR_calc(SNR, i):
            x_pix = x_min + i
            snr_local = []
            for j in range(y_max-y_min):
                y_pix = y_min+j
                # Calculate SNR
                flux = np.real(self.cube_final[x_pix, y_pix])
                flux = flux[np.where(flux != 0.0)]
                n = len(flux)
                if method == 1:
                    signal = np.max(flux)-np.median(flux)
                    noise = np.std(flux)
                    snr = float(signal / np.sqrt(noise))
                    snr = snr/(np.sqrt(np.mean(flux)))
                else:
                    # Select spectral region around Halpha and NII complex
                    min_ = np.argmin(np.abs(np.array(self.spectrum_axis)-15150))
                    max_ = np.argmin(np.abs(np.array(self.spectrum_axis)-15300))
                    flux_in_region = np.sum(self.cube_final[x_pix, y_pix, min_:max_])
                    # Select distance region
                    min_ = np.argmin(np.abs(np.array(self.spectrum_axis)-14800))
                    max_ = np.argmin(np.abs(np.array(self.spectrum_axis)-14850))
                    std_out_region = np.std(self.cube_final[x_pix, y_pix, min_:max_])
                    snr = float(flux_in_region/np.sqrt(std_out_region))
                    snr = snr#/(np.sqrt(np.mean(flux_in_region)))
                snr_local.append(snr)
            SNR[i] = snr_local
        n_threads = 16
        Parallel(n_jobs=n_threads, backend="threading", batch_size=int((x_max-x_min)/n_threads))(delayed(SNR_calc)(SNR,i) for i in tqdm(range(x_max-x_min)));
        end = time.time()
        # Save
        fits.writeto(self.output_dir+'/'+self.object_name+'_SNR.fits', SNR.T, self.header, overwrite=True)
