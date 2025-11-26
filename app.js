import React from 'react';
import { SafeAreaView, StyleSheet, View } from 'react-native';
import PhotoFrame from './components/PhotoFrame';
import RadioPlayer from './components/RadioPlayer';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <PhotoFrame />
      <RadioPlayer />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
