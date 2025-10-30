import React from 'react'
import { View, StyleSheet, Button } from 'react-native'
import { useRouter } from 'expo-router'
import GachaButton from '../../components/GachaButton'

const Pull = (): JSX.Element => {
    const router = useRouter()

    const handleNavigateHome = React.useCallback(() => {
        router.replace('/')
    }, [router])

    return (
        <View style={styles.container}>
            <View style={styles.actionArea}>
                <Button title="ホームに戻る" onPress={handleNavigateHome} />
            </View>
            <View style={styles.buttonWrapper}>
                <GachaButton />
            </View>
        </View>
    )
}

export default Pull

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F0E3',
        padding: 20,
    },
    actionArea: {
        alignSelf: 'stretch',
    },
    buttonWrapper: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
})
