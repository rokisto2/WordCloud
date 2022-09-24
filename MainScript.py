import os
import shutil


def passage(file_name, folder):
    for element in os.scandir(folder):
        if element.is_file():
            if element.name == file_name:
                yield folder
        else:
            yield from passage(file_name, element.path)


def generated_json_out():
    for filename in os.listdir("Img_in"):
        id = filename[:-4]
        s = str(*passage(f'{id}.json', 'mnt/HC_Volume_22862748'))

        shutil.copyfile(f'{s}/{id}.json', f"Json_out/{id}.json")


def generated_img_out():
    for filename in os.listdir("Json_in"):
        id = filename[:-5]
        s = str(*passage(f'{id}.png', 'mnt/HC_Volume_22862748'))

        shutil.copyfile(f'{s}/{id}.png', f"Img_out/{id}.png")


if __name__ == '__main__':
    while True:
        type = input('Choose what you want to copy\nP/p - pictures\nJ/j - json\n')
        if type.lower() == 'j':
            generated_json_out()
            break
        elif type.lower() == 'p':
            generated_img_out()
            break
