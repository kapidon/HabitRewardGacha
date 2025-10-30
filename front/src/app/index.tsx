import React from 'react'
import { StyleSheet, View, Button } from 'react-native'
import { useRouter } from 'expo-router'

const Home = (): JSX.Element => {
    const router = useRouter()

    const handleNavigateToGacha = React.useCallback(() => {
        router.push('/gacha/pull')
    }, [router])

    return (
        <View style={styles.container}>
            <View style={styles.actionArea}>
                <Button title="ガチャを引く" onPress={handleNavigateToGacha} />
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFFFFF',
        padding: 24,
    },
    actionArea: {
        alignSelf: 'stretch',
    },
})

export default Home
