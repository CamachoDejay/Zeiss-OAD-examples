#################################################################
# File        : CD7_3_Slides
# Version     : 1.0
# Author      : camachodejay
# Date        : 2023-02-27
# Institution : Centre for Cellular Imaging, Gothenburg University
#
# Script designed for the CD7. It allows to use the 3 slide insert, 
# select the experiment to perform at each slide and then run the 
# expeiments sequentially.
#
# Based on examples at https://github.com/zeiss-microscopy/OAD
# 
# Note, there is still some small TODO. This is a beta release
# Tested with ZEN blue 3.2
###################################################################

import time
from datetime import datetime
from System.IO import File, Directory, Path


macro_name = 'CD7 3 slides'
# version number for dialog window
version = 1.0
# delay for specific hardware movements in [seconds]
hwdelay = 1
# experiment blockindex, related to tiles
blockindex = 0

def GetDateTimeStringForFilename(dt = None):
    """ Get the current date and time in a formatted string
    """
    if(dt == None):
        dt = datetime.now()
    strDateTimeCurrent = dt.strftime('%Y-%m-%d_%H-%M-%S')
    return strDateTimeCurrent

def getshortfiles(filelist):
    """Create list with shortended filenames

    :param filelist: List with files with complete path names
    :type filelist: list
    :return: List with filenames only
    :rtype: list
    """
    files_short = []
    for short in filelist:
        files_short.append(Path.GetFileName(short))

    return files_short

def printFileList(filelist):
    """Print elements of file list"""
    
    for item in filelist:
        print item

    return True

def createfolder(basedir, formatstring='%Y-%m-%d_%H-%M-%S'):
    """Creates a new folder inside an existing folder using a specific format

    :param basedir: Folder inside which the new directory should be created
    :type basedir: str
    :param formatstring: String format for the new folder, defaults to '%Y-%m-%d_%H-%M-%S'
    :type formatstring: str, optional
    :return: Newly created directory
    :rtype: str
    """    

    # construct new directory name based on date and time
    newdir = Path.Combine(basedir, datetime.now().strftime(formatstring))
    # check if the new directory (for whatever reasons) already exists
    try:
        newdir_exists = Directory.Exists(newdir)
        if not newdir_exists:
            # create new directory if is does not exist
            Directory.CreateDirectory(newdir)
        if newdir_exists:
            # raise error if it really already exists
            raise SystemExit
    except OSError as e:
        if e.errno != errno.EEXIST:
            newdir = None
            raise  # This was not a "directory exist" error..

    return newdir


def dircheck(basefolder):
    """Check if a directory or folder already exits.
    Create the folder if it does not exist

    :param basefolder: folder to check
    :type basefolder: str
    :return: new_directory
    :rtype: str
    """

    # check if the destination basefolder exists
    base_exists = Directory.Exists(basefolder)

    if base_exists:
        print('Selected Directory Exists: ', base_exists)
        # specify the desired output format for the folder, e.g. 2017-08-08_17-47-41
        format = '%Y-%m-%d_%H-%M-%S'
        
        # create the new directory
        newdir = createfolder(basefolder, formatstring=format)
        print('Created new directory: ', newdir)
    
    if not base_exists:
        Directory.CreateDirectory(basefolder)
        newdir = basefolder

    return newdir

def cloneexp(expname, prefix='GA_', save=True, reloadexp=True):
    """Clone an existing ZenExperiment.

    :param expname: Name of the ZenExperiment
    :type expname: ZenExperiment
    :param prefix: Prefix for the experiment name, defaults to 'GA_'
    :type prefix: str, optional
    :param save: Option to save the cloned experiment, defaults to True
    :type save: bool, optional
    :param reloadexp: option to reload the cloned experiment afterwards, defaults to True
    :type reloadexp: bool, optional
    :return: exp_reload
    :rtype: ZenExperiment or None
    """

    exp = Zen.Acquisition.Experiments.GetByName(expname)
    exp_newname = prefix + expname

    # save experiment
    if save:
        exp.SaveAs(exp_newname, False)
        print('Saved Temporay Experiment as : ', exp_newname)
        # close the original experiment object
        exp.Close()
        time.sleep(1)
    
    # reload experiment
    if reloadexp:
        exp_reload = Zen.Acquisition.Experiments.GetByName(exp_newname)
    elif not reloadexp:
        exp_reload = None

    return exp_reload

def testSnap(active_exp, close_snap = True):
    """Does a test snap to load some experimental settings such as the objective and TL.
    
    :param active_exp: ZenExperiment which is loaded and active"""
    
    # test snap to change to the valid settings, e.g. the objective from the DetailScan
    testsnap = Zen.Acquisition.AcquireImage(active_exp)
    
    print('Acquire Test Snap using: TODO ADD')
    if close_snap:
        testsnap.Close()
    else:
        # show the overview scan inside the document area
        Zen.Application.Documents.Add(testsnap)
        print('Snap remains open')
        
    # wait for moving hardware due to settings
    time.sleep(hwdelay)
    return True


def GetZenVersionAsFloat():
    """Get the current major &amp; minor ZEN version as a floating point number for comparisons."""
    version = 0.0
    try:
        strVer = Zen.Application.Environment.Version
        strsVer = strVer.Split('.')
        if(strsVer.Length &gt;= 2):
            strVerMajMin = strsVer[0] + "." + strsVer[1]
            version = float(strVerMajMin)
    except:
        version = 0.0
    return version


def IsInstrumentCD7(defaultValue = False):
    """ Detect whether the current instrument is a CD7 """
    cd7 = defaultValue
    #--- Get ZEN Blue Version ---
    verZen = GetZenVersionAsFloat()
    #--- This technique only works with ZEN 3.1 or later ---
    if(verZen &gt;= 3.1):
        try:
            zls = ZenLiveScan
        except:
            zls = None
        if (zls == None):
            cd7 = False
        else:
            cd7 = True
    else:
        #--- This technique does not work with the current ZEN version ---
        print('Automatic CD7 detection requires ZEN 3.1 or greater.')
        print('Current ZEN Version: ', Zen.Application.Environment.Version, ' (', str(verZen), ')')
    return cd7
    
def changeCD7Slide3x76(Slide = 'A1'):
    """Detects if microscope is a CD7 and then changes the slide position to A1, A2 or A3"""
    assert IsInstrumentCD7(), 'This is not CD7 so we get out'
    
    #--- Prepare the Slide Settings ---
    hwSetting = ZenHardwareSetting()
    
    # hardwaresetting1.SetParameter('MTBLiveCellScanner', 'StagePosition', 'ScanSlide76Left')
    # hardwaresetting1.SetParameter('MTBLiveCellScanner', 'StagePosition', 'ScanSlide76Center')
    # hardwaresetting1.SetParameter('MTBLiveCellScanner', 'StagePosition', 'ScanSlide76Right')
    if Slide == 'A1':
        StagePos_str = 'ScanSlide76Left'
    elif Slide == 'A2':
        StagePos_str = 'ScanSlide76Center'
    elif Slide == 'A3':
        StagePos_str = 'ScanSlide76Right'
    else:
        raise Exception('Execution stopped. I do not understand slide position')
        
    hwSetting.SetParameter('MTBLiveCellScanner', 'StagePosition', StagePos_str)
    
    Zen.Devices.ApplyHardwareSetting(hwSetting)

    return True

def runExpInSlide(SlidePosition, ExpSettings_name):
    """Runs slide with settings TODO add info"""
    
    changeCD7Slide3x76(SlidePosition)

    # create a duplicate of the OVScan experiment to work with
    Exp_reloaded = cloneexp(ExpSettings_name)
    
    # active the temporary experiment to trigger its validation
    Exp_reloaded.SetActive()
    time.sleep(hwdelay)
    
    # check if the experiment contains tile regions
    SlideIsTileExp = Exp_reloaded.IsTilesExperiment(blockindex)
    
    # test snap to change to the valid settings, e.g. the objective from the DetailScan
    testSnap(Exp_reloaded)
    
    # initial focussing via FindSurface to assure a good starting position
    Zen.Acquisition.FindSurface()
    print('Z-Position after FindSurface: ', Zen.Devices.Focus.ActualPosition)
    
    # test snap to change to the valid settings, e.g. the objective from the DetailScan
    testSnap(Exp_reloaded)
    
    # execute the experiment
    print('Running Experiment: ', ExpSettings_name)
    
    camerasetting1 = ZenCameraSetting()
    camerasetting1.SetParameter('SoftwareBinningList', '4')
    Zen.Acquisition.ActiveCamera.ApplyCameraSetting(camerasetting1)
    
    output_S = Zen.Acquisition.Execute(Exp_reloaded)
    
    # show the overview scan inside the document area
    #Zen.Application.Documents.Add(output_S)
    doc = Zen.Application.Documents.GetByName(output_S.Name)
    
    camerasetting1.SetParameter('SoftwareBinningList', '0')
    Zen.Acquisition.ActiveCamera.ApplyCameraSetting(camerasetting1)
    
    return doc
    
def setSoftwareBinning(active_exp,bin = 1):
    """gets an active experiment modifies the Software Binning, this is the param in
    Hardware Specific"""
    # TODO: finish this one
    
    cam_set = ZenCameraSetting()
    if bin == 1:
        bin_idx = '0'
    elif bin == 5:
        bin_idx = '4'
    else:
        raise Expection('Do not understand the binning request') 
        
    cam_set.SetParameter('SoftwareBinningList', bin_idx)
    Zen.Acquisition.ActiveCamera.ApplyCameraSetting(cam_set)
    
    active_exp = Zen.Acquisition.Experiments.GetByName(expname)
    active_exp.Save()
    

    return active_exp


###########################################################################

# clear console output
Zen.Application.MacroEditor.ClearMessages()

# check the location of experiment setups and image analysis settings are stored
docfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.UserDocuments)
imgfolder = Zen.Application.Environment.GetFolderPath(ZenSpecialFolder.ImageAutoSave)
imgfolder = r'D:\CCI users\RafaCCI\Automated_testing'
format = '%Y-%m-%d_%H-%M-%S'

# get list with all existing experiments and image analysis setup and a short version of that list
expfiles = Directory.GetFiles(Path.Combine(docfolder, 'Experiment Setups'), '*.czexp')
ipfiles = Directory.GetFiles(Path.Combine(docfolder, 'Image Analysis Settings'), '*.czias')
apfiles = Directory.GetFiles(Path.Combine(docfolder, 'APEER Module Settings'), '*.czams')
expfiles_short = getshortfiles(expfiles)
ipfiles_short = getshortfiles(ipfiles)
apfiles_short = getshortfiles(apfiles)

print 'User doc folder: ', docfolder

#printFileList(expfiles_short)

# Initialize Dialog
GuidedAcqDialog = ZenWindow()
GuidedAcqDialog.Initialize(macro_name + ' v_beta_' + str(version))
# add components to dialog
GuidedAcqDialog.AddLabel('------   Select Experiment Slide 1  ------')
GuidedAcqDialog.AddDropDown('S1_exp', 'Slide 1 Experiment', expfiles_short, 0)

GuidedAcqDialog.AddLabel('------   Select Experiment Slide 2  ------')
GuidedAcqDialog.AddDropDown('S2_exp', 'Slide 2 Experiment', expfiles_short, 0)

GuidedAcqDialog.AddLabel('------   Select Experiment Slide 3  ------')
GuidedAcqDialog.AddDropDown('S3_exp', 'Slide 3 Experiment', expfiles_short, 0)

GuidedAcqDialog.AddLabel('------   Specify basefolder to save the images   ------')
GuidedAcqDialog.AddFolderBrowser('outfolder', 'Basefolder for Images and Data Tables', imgfolder)

# show the window
result = GuidedAcqDialog.Show()
if result.HasCanceled:
    message = 'Macro was canceled by user.'
    print(message)
    raise SystemExit

# get the values and store them
S1ExpName = str(result.GetValue('S1_exp'))
S2ExpName = str(result.GetValue('S2_exp'))
S3ExpName = str(result.GetValue('S3_exp'))
OutputFolder = str(result.GetValue('outfolder'))

# check directory, and create new subfolder with timestamp
OutputFolder = dircheck(OutputFolder)

print 'Output Folder for Data : ', OutputFolder
print('\n')


# run fisrt slide
A1_doc = runExpInSlide('A1', S1ExpName)
# save the overview scan image inside the select folder
S_name = 'A1.czi'
savepath_S = Path.Combine(OutputFolder, S_name)
A1_doc.Save(savepath_S)

# run second slide
A2_doc = runExpInSlide('A2', S2ExpName)
# save the overview scan image inside the select folder
S_name = 'A2.czi'
savepath_S = Path.Combine(OutputFolder, S_name)
A2_doc.Save(savepath_S)

# run third slide
A3_doc = runExpInSlide('A3', S3ExpName)
# save the overview scan image inside the select folder
S_name = 'A3.czi'
savepath_S = Path.Combine(OutputFolder, S_name)
A3_doc.Save(savepath_S)