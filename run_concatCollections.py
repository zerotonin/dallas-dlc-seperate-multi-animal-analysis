import yaml,pandas,os

archiveDir    = '/media/dataSSD/AnkaArchive'
yamlDir

#get all files that were analysed by this AI in source directory
yamlFiles_files = [f for f in os.listdir(yamlDir) if f.endswith(.yaml)]