import { BtnRegister } from "@/components/button";
import { Input } from "@/components/input";
import { Link } from "expo-router";
import { StyleSheet, Text, View } from "react-native";

export default function Index() {
  return (
    <View style={styles.container}>
      <Text style={styles.tittle}>Login</Text>
      <Input placeholder="E-mail" />
      <Input placeholder="Password" />
      <BtnRegister label="Submit" />
      <Text>
        Não se cadastrou?{" "}
        <Link style={styles.link} href="/register">
          Cadastre-se Aqui
        </Link>
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
    gap: 15,
    padding: 15,
  },
  tittle: {
    fontSize: 30,
    fontWeight: "bold",
  },
  link: {
    color: "blue",
  },
});
