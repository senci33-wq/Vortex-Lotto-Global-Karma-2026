import React from "react";
import {
  ImageBackground,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import * as WebBrowser from "expo-web-browser";

import { Colors, Fonts, Images, Radius, Spacing } from "@/constants/theme";

const CONTACT = "vortex-lotto-feedback@gmail.com";

export default function VisionScreen() {
  const insets = useSafeAreaInsets();

  const openMail = async () => {
    const url = `mailto:${CONTACT}`;
    if (Platform.OS === "web") window.open(url, "_blank");
    else await WebBrowser.openBrowserAsync(url);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: Spacing.xxxl }}>
      <ImageBackground
        source={{ uri: Images.visionBg }}
        style={[styles.hero, { paddingTop: insets.top + Spacing.xxl }]}
      >
        <LinearGradient
          colors={["rgba(2,6,23,0.4)", "rgba(2,6,23,0.95)"]}
          style={StyleSheet.absoluteFill}
        />
        <Text style={styles.heroTitle} allowFontScaling={false}>
          DIE VORTEX-VISION
        </Text>
        <Text style={styles.heroSub} allowFontScaling={false}>
          Einklang &amp; Verantwortung
        </Text>
      </ImageBackground>

      <View style={styles.body}>
        <Section title="Unser blauer Planet" icon="earth">
          Bevor wir uns als Spezies weiter in das Universum wagen, liegt unsere höchste Priorität
          darin, unser gemeinsames Zuhause in Ordnung zu bringen. Technischer Fortschritt ist nur
          dann wertvoll, wenn er im Einklang mit allen Lebewesen auf diesem Planeten geschieht.
        </Section>

        <Section title="Globales Karma & Quanten-Technik" icon="flash">
          Wir nutzen die Sprache des Universums – den Quanten-Zufall –, um hier auf der Erde Chancen
          zu verteilen und Aufmerksamkeit auf Projekte zu lenken, die oft übersehen werden.
          Inklusion für Regionen ohne feste Infrastruktur und direkte Unterstützung von Initiativen
          wie der Sanfilippo Initiative, der Augsburger Tafel und globalen Wasserprojekten.
        </Section>

        <Section title="Der Weg zu den Sternen" icon="planet">
          Die Erforschung des Kosmos ist ein wichtiges Ziel der Menschheit. Doch wir gehen diesen Weg
          nicht als Flüchtlinge von einer zerstörten Welt, sondern als Botschafter eines geheilten
          Planeten.
        </Section>

        <View style={styles.quoteCard}>
          <Text style={styles.quote} allowFontScaling={false}>
            „Erst die Heimat heilen, dann die Sterne erreichen – im Einklang mit allem, was lebt.“
          </Text>
        </View>

        <View style={styles.divider} />

        <Text style={styles.privacyHeading} allowFontScaling={false}>
          DATENSCHUTZ
        </Text>
        <Section title="Keine Datenerhebung" icon="lock-closed">
          Diese App ist ein Non-Profit-Projekt. Sie erhebt, speichert oder überträgt keinerlei
          personenbezogene Daten. Es gibt keine Registrierung und kein Tracking.
        </Section>
        <Section title="Drittanbieter" icon="server">
          Für echten Zufall wird eine technische Anfrage an den Quanten-Server der ANU (Australian
          National University) gestellt. Es werden keine Nutzerprofile erstellt.
        </Section>
        <Section title="Externe Links" icon="link">
          Über die Karma-Projekte wirst du zu externen Webseiten von Spendenorganisationen
          weitergeleitet. Für deren Inhalte sind die jeweiligen Betreiber verantwortlich.
        </Section>

        <Pressable style={styles.contactBtn} onPress={openMail} testID="contact-button">
          <Ionicons name="mail-outline" size={20} color={Colors.brand} />
          <Text style={styles.contactText} allowFontScaling={false}>
            {CONTACT}
          </Text>
        </Pressable>

        <Text style={styles.footer} allowFontScaling={false}>
          Vortex Lotto Global Karma 2026 · Non-Profit · Open Source
        </Text>
      </View>
    </ScrollView>
  );
}

function Section({
  title,
  icon,
  children,
}: {
  title: string;
  icon: keyof typeof Ionicons.glyphMap;
  children: string;
}) {
  return (
    <View style={styles.section}>
      <View style={styles.sectionHead}>
        <Ionicons name={icon} size={18} color={Colors.brand} />
        <Text style={styles.sectionTitle} allowFontScaling={false}>
          {title}
        </Text>
      </View>
      <Text style={styles.sectionBody}>{children}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.surface },
  hero: { paddingHorizontal: Spacing.xl, paddingBottom: Spacing.xl, minHeight: 180 },
  heroTitle: {
    fontFamily: Fonts.displayBold,
    fontSize: 30,
    color: Colors.brand,
    letterSpacing: 1.5,
  },
  heroSub: { fontFamily: Fonts.bodyMedium, fontSize: 14, color: Colors.onSurfaceSecondary },
  body: { padding: Spacing.xl, gap: Spacing.xl },
  section: { gap: Spacing.sm },
  sectionHead: { flexDirection: "row", alignItems: "center", gap: Spacing.sm },
  sectionTitle: { fontFamily: Fonts.displaySemi, fontSize: 18, color: Colors.onSurface },
  sectionBody: {
    fontFamily: Fonts.body,
    fontSize: 15,
    lineHeight: 23,
    color: Colors.onSurfaceSecondary,
  },
  quoteCard: {
    backgroundColor: "rgba(34,211,238,0.08)",
    borderLeftWidth: 3,
    borderLeftColor: Colors.brand,
    borderRadius: Radius.md,
    padding: Spacing.lg,
  },
  quote: {
    fontFamily: Fonts.displayMedium,
    fontSize: 18,
    lineHeight: 26,
    color: Colors.onSurface,
    fontStyle: "italic",
  },
  divider: { height: 1, backgroundColor: Colors.border, marginVertical: Spacing.sm },
  privacyHeading: {
    fontFamily: Fonts.displayBold,
    fontSize: 20,
    color: Colors.onSurfaceSecondary,
    letterSpacing: 2,
  },
  contactBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: Spacing.sm,
    backgroundColor: Colors.surfaceSecondary,
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: Radius.lg,
    paddingVertical: Spacing.lg,
  },
  contactText: { fontFamily: Fonts.bodyMedium, fontSize: 15, color: Colors.brand },
  footer: {
    fontFamily: Fonts.body,
    fontSize: 12,
    color: Colors.onSurfaceTertiary,
    textAlign: "center",
  },
});
