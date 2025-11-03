import React from 'react'
import { View, StyleSheet } from 'react-native'
import { Stack } from 'expo-router'
import { SafeAreaProvider } from 'react-native-safe-area-context'
import FooterNavigation from '../components/FooterNavigation'

// フッターの高さをコンテンツ側で確保するための定数
const FOOTER_RESERVED_HEIGHT = 72

const Layout = (): JSX.Element => {
    return (
        <SafeAreaProvider>
            <View style={styles.container}>
                <Stack screenOptions={{
                    headerStyle: {
                        backgroundColor: '#467FD3'
                    },
                    headerTintColor: '#FFFFFF',
                    headerTitle: 'RewardGacha',
                    headerBackTitle: 'Back',
                    headerTitleStyle: {
                        fontSize: 22,
                        fontWeight: 'bold'
                    },
                    contentStyle: {
                        paddingBottom: FOOTER_RESERVED_HEIGHT + 16
                    }
                }} />
                <FooterNavigation reservedHeight={FOOTER_RESERVED_HEIGHT} />
            </View>
        </SafeAreaProvider>
    )
}

export default Layout

const styles = StyleSheet.create({
    container: {
        flex: 1
    }
})
