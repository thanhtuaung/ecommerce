import uuid

def generate_filename(instance, filename):
    # Get the file extension from the original filename
        ext = filename.split('.')[-1]
        
        # Generate a unique filename using UUID and the original extension
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        
        return new_filename
