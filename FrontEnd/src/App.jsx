import { useState } from "react";

export default function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async () => {
    if (!image) {
      alert("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Upload failed");
      }
      
      const data = await response.json();
      setProcessedImage(`http://localhost:5000/${data.processed_image}`);
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
        YOLO Object Detection
      </h1>
      
      {/* Image upload section */}
      <div className="flex flex-col items-center gap-6 mb-8">
        <label className="cursor-pointer">
          <span className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 transition">
            Choose Image
          </span>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageChange} 
            className="hidden"
          />
        </label>
        {preview && (
          <div className="w-full max-w-md rounded-lg overflow-hidden shadow-lg">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-auto object-cover"
            />
          </div>
        )}
      </div>

      {/* Upload and process button */}
      <button 
        className="px-8 py-3 bg-purple-600 text-white rounded-lg shadow-lg hover:bg-purple-700 transition"
        onClick={handleUpload}
      >
        Upload and Process
      </button>

      {/* Processed image */}
      {processedImage && (
        <div className="mt-8 w-full max-w-md rounded-lg overflow-hidden shadow-lg">
          <h2 className="text-2xl font-semibold text-center mb-4 text-gray-800">
            Processed Image
          </h2>
          <img 
            src={processedImage} 
            alt="Processed" 
            className="w-full h-auto object-cover"
          />
        </div>
      )}
    </div>
  );
}