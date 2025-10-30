import React from 'react'
import { Stack } from 'expo-router'

const Layout = (): JSX.Element => (
    <Stack
        screenOptions={{
            headerStyle: {
                backgroundColor: '#467FD3',
            },
            headerTintColor: '#ffffff',
            headerTitle: 'RewardGacha',
            headerBackTitle: 'Back',
            headerTitleStyle: {
                fontSize: 22,
                fontWeight: 'bold',
            },
        }}
    />
)

export default Layout
