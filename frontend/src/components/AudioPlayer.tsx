import React, { useEffect, useRef } from 'react';

interface AudioPlayerProps {
  audioStreamUrl: string;
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioStreamUrl }) => {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (!audioRef.current) return;

    audioRef.current.src = audioStreamUrl;

    audioRef.current.play().catch((error) => {
      console.error('Error playing audio:', error);
    });

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
      }
    };
  }, [audioStreamUrl]);


  return <audio ref={audioRef} />;
};

export default AudioPlayer;
