import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { Audio } from 'expo-av';

const streamUrl = 'http://fm983.cityfm.tw:8080/983.mp3'; // 可替換成其他串流

export default function RadioPlayer() {
  const [sound, setSound] = React.useState(null);

  const playRadio = async () => {
    const { sound } = await Audio.Sound.createAsync({ uri: streamUrl });
    setSound(sound);
    await sound.playAsync();
  };

  const stopRadio = async () => {
    if (sound) {
      await sound.stopAsync();
      await sound.unloadAsync();
      setSound(null);
    }
  };

  return (
    <View style={styles.player}>
      <Text style={styles.label}>FM 收音機：FM98.3 城市廣播</Text>
      <View style={styles.buttons}>
        <Button title="播放" onPress={playRadio} />
        <Button title="停止" onPress={stopRadio} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  player: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  label: {
    fontSize: 16,
    marginBottom: 10,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
});
