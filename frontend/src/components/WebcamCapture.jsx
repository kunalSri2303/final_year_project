import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
};

function WebcamCapture({ onCapture, disabled }) {
  const webcamRef = useRef(null);
  const [isOn, setIsOn] = useState(false);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      onCapture(imageSrc);
    }
  }, [webcamRef, onCapture]);

  if (!isOn) {
    return (
      <div className="webcam-container">
        <button className="btn secondary" onClick={() => setIsOn(true)}>
          Enable Camera
        </button>
      </div>
    );
  }

  return (
    <div className="webcam-container">
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
        className="webcam-element"
      />
      <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn" onClick={capture} disabled={disabled}>
            Snap & Detect
          </button>
          <button className="btn secondary" onClick={() => setIsOn(false)}>
            Turn Off
          </button>
      </div>
    </div>
  );
}

export default WebcamCapture;
