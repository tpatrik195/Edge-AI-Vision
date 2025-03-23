import React from "react";

const BackgroundSelector = ({ setImageURL }) => {
  const handleImageUpload = (e) => {
    const reader = new FileReader();
    reader.onload = () => setImageURL(reader.result);
    reader.readAsDataURL(e.target.files[0]);
  };

  return (
    <div className="backgroundSelector">
      <input type="file" accept="image/*" onChange={handleImageUpload} />
    </div>
  );
};

export default BackgroundSelector;
