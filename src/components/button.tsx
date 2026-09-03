import {
    StyleSheet,
    Text,
    TouchableOpacity,
    TouchableOpacityProps,
} from "react-native";

type ButtonProps = TouchableOpacityProps & {
  label: string;
};

export function BtnRegister({ label, ...rest }: ButtonProps) {
  return (
    <TouchableOpacity style={styles.btn} {...rest}>
      <Text style={styles.label}>{label}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  btn: {
    alignItems: "center",
    justifyContent: "center",
    width: "50%",
    backgroundColor: "pink",
    borderRadius: 15,
    padding: 10,
  },
  label: {
    fontSize: 25,
    fontWeight: "bold",
  },
});
