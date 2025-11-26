import React, { useState, useEffect } from 'react';
import { View, Image, StyleSheet } from 'react-native';

const samplePhotos = [
  require('../assets/photo1.jpg'),
  require('../assets/photo2.jpg'),
  require('../assets/photo3.jpg'),
];

export default function PhotoFrame() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % samplePhotos.length);
    }, 5000); // 每 5 秒切換
    return () => clearInterval(timer);
  }, []);

  return (
    <View style={styles.frame}>
      <Image source={samplePhotos[index]} style={styles.image} resizeMode="cover" />
    </View>
  );
}

const styles = StyleSheet.create({
  frame: {
    flex: 2,
    borderBottomWidth: 1,
    borderColor: '#ccc',
  },
  image: {
    width: '100%',
    height: '100%',
  },
});
