import React from 'react'
import { View, StyleSheet } from 'react-native'
import GachaButton from '../../components/GachaButton'

const Pull = (): JSX.Element => {
    return (
        <View style={styles.container}>
            <GachaButton />
        </View>
    )
}

export default Pull

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F0E3',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    }
});