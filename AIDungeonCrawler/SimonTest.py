from openai import OpenAI
import pygame
from PIL import Image
import io
import requests
client = OpenAI(api_key = "sk-proj-MduORQWiwbEHFJDHNQnLT3BlbkFJzXOJKG2q6utiMNOtx3ID")

response = client.images.generate(
  model = "dall-e-3",
  prompt = "90's grid based dungeon crawler enemy",
  size = "1024x1024",
  quality = "standard",
  n=1,
)

image_url = response.data[0].url
#image.urlretrieve(image_url, "image.png") #specify path
print(image_url)

response = requests.get(image_url)
img = Image.open(io.BytesIO(response.content))

#img.show()

pygame.image.load(io.BytesIO(response.content))