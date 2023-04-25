import os
import cartoonization_methods
import shutil

current_dir = os.getcwd()
cartoonization_log = '/../logs/cartoonization.log'
cartoonization_log_path = current_dir + cartoonization_log

method_used = []

with open (cartoonization_log_path, 'r') as log:
    lines = iter(log.readlines())
    for line in lines:
        if '../data/renamed_images\\' in line:
            image_name = line.split(',')[0].split('\\')[-1]
            next_line = next(lines)
            method = next_line.split()[-1]
            method_used.append((image_name, method))

# Retrieve the cartoonization methods defined in the module (they all start by cartoonizer_)
methods = [element for element in dir(cartoonization_methods) if 'cartoonizer_' in element]
# print('Methods:', methods)

# Get the methods indices (those saved in method_used)
method_indices = list(map(lambda x: x[-1], methods))
# print('Indices:', method_indices)

# Create folders containing transformed images per method
import cartoonization_methods
data_dir = os.path.join(current_dir, '../data')
for index in method_indices:
    folder_name = 'transformed_' + index
    folder_path = os.path.join(data_dir, folder_name)
    ### Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
#             msg = transformed_images_dir + ' created successfully'
#             print(msg), logger.info(msg)
        except Exception as e:
#             print(e), logger.error(e)
            sys.exit()
    ### Delete everything inside it otherwise
    else:
#         msg = f'Folder {folder_path} already exist'
#         print(msg), logger.info(msg)
#         msg = 'Emptying it'
#         print(msg), logger.info(msg)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
#                 msg = f'Failed to delete {file_path}. Reason: {e}'
#                 print(msg), logger.error(msg)
                sys.exit()
#         msg = 'Done'
#         print(msg), logger.info(msg)
    
    # Once the folder created, fill it with corresponding images
    folder_images = [method[0] for method in method_used if method[1] == index]
    src = os.path.join(data_dir, 'transformed_images')
    dst = folder_path
    for image in folder_images:
        shutil.copy(os.path.join(src, image), dst)