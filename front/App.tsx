import React from 'react'
import { ExpoRoot } from 'expo-router'

export default function App(): JSX.Element {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-var-requires
    // @ts-expect-error Expo Router injects the require.context helper at runtime
    const ctx = require.context('./src/app')
    return <ExpoRoot context={ctx} />
}
