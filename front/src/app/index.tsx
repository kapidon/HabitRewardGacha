import React from 'react'
import { View, Text, StyleSheet } from 'react-native'

const Index = (): JSX.Element => {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>RewardGachaへようこそ</Text>
            <Text style={styles.description}>下部のガチャアイコンからガチャを引いてみましょう。</Text>
        </View>
    )
}

export default Index

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#F8F0E3',
        paddingHorizontal: 24
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#2C3E50',
        marginBottom: 12
    },
    description: {
        fontSize: 16,
        color: '#34495E',
        textAlign: 'center',
        lineHeight: 22
    }
})
