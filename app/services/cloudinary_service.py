import cloudinary.uploader

#Esta función me regresa la url de mi imagen que estará en Cloudinary.
#Esto es posible ya que instalé algo relacionado a su API que me ayuda a hacer las peticiones sin tanto problema.
def upload_image_to_cloudinary(file) -> str:
    result = cloudinary.uploader.upload(file)
    return result["secure_url"]