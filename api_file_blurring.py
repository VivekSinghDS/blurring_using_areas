import face_recognition
import cv2
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from pydantic import BaseModel


def blur_it(IMAGE_PATH):
    image = face_recognition.load_image_file(IMAGE_PATH)
    x = face_recognition.face_locations(image)
    print(x)
    d = {}
    for idx, tuple in enumerate(face_recognition.face_locations(image)):
        # print(idx)

        top, right, bottom, left = tuple
        # print(top, right, bottom, left)
        d[idx] = (bottom - top) * (right - left)
        # image[top:bottom, left:right] = cv2.blur(image[top:bottom, left:right], (40, 40))

    print(d)
    if (d == {}):
        print('No face detected')
        return IMAGE_PATH
    else:
        maximum_area = max(d.values())
        del d
        # sorted_values = dict(sorted(d.items(), key=lambda item: item[1]))
        # print('sorted values dict is ')
        # print(sorted_values)

        for idx, tuple in enumerate(face_recognition.face_locations(image)):
            # print(idx)

            top, right, bottom, left = tuple
            if (((bottom - top) * (right - left) / maximum_area) * 100 < 41.0):
                image[top:bottom, left:right] = cv2.blur(image[top:bottom, left:right], (40, 40))

            else:
                print('Area significant to the main image')
                print(((bottom - top) * (right - left) / maximum_area) * 100, ' is the percentage of ', maximum_area)
                continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('blurred_' + IMAGE_PATH, image)
        return ('blurred_' + IMAGE_PATH, image)
    # img = cv2.imread('test4.jpeg')
    # image = face_recognition.load_image_file("test4.jpeg")



app = FastAPI()
class Item(BaseModel):
    image_path:str

@app.post('/blur_image/')
async def create_item(item:Item):
    item_dict = item.dict()
    print('i am here')
    print(item_dict['image_path'])
    # test('test/img3.jpeg')
    x = blur_it(item_dict['image_path'])
    if(x == item_dict['image_path']):
        return FileResponse(x)
    # if('/' in item_dict['image_path']):
    #     item_dict['image_path'] = item_dict['image_path'].split('/')[-1]
    return FileResponse(x)



@app.get('/',status_code=status.HTTP_200_OK)
async def root():
    return "smart blurring"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)