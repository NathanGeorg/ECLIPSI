import { StyleSheet, TextInput, TextInputProps } from "react-native";

export function Input({ ...rest }: TextInputProps) {
  return (
    <TextInput style={styles.input} placeholderTextColor="gray" {...rest} />
  );
}

const styles = StyleSheet.create({
  input: {
    width: "100%",
    borderColor: "pink",
    borderWidth: 1,
    borderRadius: 15,
    height: 40,
    padding: 10,
  },
});
