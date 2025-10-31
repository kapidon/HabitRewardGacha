import React, { useEffect } from 'react'
import { Stack } from 'expo-router'

import { initializeHabitTable } from '../database/habitTable'

const Layout = (): JSX.Element => {
    useEffect(() => {
        void initializeHabitTable().catch((error) => {
            console.error('Failed to initialize habit table', error)
        })
    }, [])

    return (
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
}

export default Layout
