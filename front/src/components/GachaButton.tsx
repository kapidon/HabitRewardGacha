import React, { useRef, useState } from 'react'
import { useRouter } from 'expo-router'
import { Animated, PanResponder, View, StyleSheet, Image, TouchableOpacity, Text } from "react-native";
import axios from 'axios'
import jarImage from '../../assets/jar.png'
import handImage from '../../assets/hand.png'

type Result = {
    name: string
    rarity: string
    image_url: string
    blog_url: string | null
    blog_name: string | null
    description: string | null
}

type GachaType = 'normal' | 'rare' | 'super_rare'

const fetchGachaResult = async (gachaType: GachaType): Promise<Result> => {
    const response = await axios.get<Result>(`http://10.0.2.2:8000/gacha/pull?gacha_type=${gachaType}`)
    return response.data
}

const GachaButton = (): JSX.Element => {
    const router = useRouter()
    // Animated.ValueXYはネストされたクラス、Animatedというグループでグループ化したい時に使う
    // クラスのinstance化時にnewが必要
    // useRefでレンダリング間で値（同じインスタンス）を保持しする
    // 
    
    const pan = useRef(new Animated.ValueXY()).current;
    const [isGachaProcessing, setIsGachaProcessing] = useState(false);
    const [selectedGachaType, setSelectedGachaType] = useState<GachaType>('normal');

    const handleGachaPull = async () => {
        setIsGachaProcessing(true);
        try {
            const response = await fetchGachaResult(selectedGachaType)
            Animated.spring(pan, {
                toValue: { x: 0, y: 0 },
                useNativeDriver: false,
            }).start(() => {
                setIsGachaProcessing(false);
                router.push({
                    pathname: 'gacha/result',
                    params: {
                        'name': encodeURIComponent(response.name),
                        'rarity': encodeURIComponent(response.rarity),
                        'image_url': encodeURIComponent(response.image_url),
                        'blog_url': response.blog_url ? encodeURIComponent(response.blog_url) : '',
                        'blog_name': response.blog_name ? encodeURIComponent(response.blog_name) : '',
                        'description': response.description ? encodeURIComponent(response.description) : ''
                    }
                });
            });
        } catch(e) {
            console.log('error', e);
            setIsGachaProcessing(false);
        }
    };
    // ジェスチャーイベントを定義
    const panResponder = PanResponder.create({
        // タッチした時にpanResponderをONにする
        onStartShouldSetPanResponder: () => true,
        //ユーザーがドラッグしている時に継続的に呼び出される
        onPanResponderMove: (_, gesture) => {
            // ガチャ処理中じゃない時だけハンドル操作を許可
            if (!isGachaProcessing) {
                // gesture.dyでユーザーのドラッグ距離を受け取る
                // 0~50までの縦方向移動にしかならないようにする
                pan.setValue({ x: 0, y: Math.max(0, Math.min(100, gesture.dy)) });
            }
        },
        onPanResponderRelease: (_, gesture) => {
            const adjustedDy = Math.max(0, Math.min(150, gesture.dy));
            // ガチャ中じゃなく、ハンドルの位置が50以上ならガチャを引く
            if (!isGachaProcessing && adjustedDy > 100) {
                handleGachaPull();
            } else {
                // 閾値に達していない場合は元の位置にばねのように戻す
                Animated.spring(pan, {
                    // 終了時の位置
                    toValue: { x: 0, y: 0 },
                    // transformなどのプロパティを使用するならfalse
                    useNativeDriver: false,
                }).start();
            }
        }
    });

    return (
        <View style={styles.container}>
            <View style={styles.tabContainer}>
                <TouchableOpacity 
                    // 選択されていたら、選択済みのスタイルを指定
                    style={[styles.tab, selectedGachaType === 'normal' && styles.selectedTab]}
                    onPress={() => setSelectedGachaType('normal')}
                >
                    <Text style={styles.tabText}>通常ガチャ</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                    style={[styles.tab, selectedGachaType === 'rare' && styles.selectedTab]}
                    onPress={() => setSelectedGachaType('rare')}
                >
                    <Text style={styles.tabText}>レアガチャ</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                    style={[styles.tab, selectedGachaType === 'super_rare' && styles.selectedTab]}
                    onPress={() => setSelectedGachaType('super_rare')}
                >
                    <Text style={styles.tabText}>スーパーレアガチャ</Text>
                </TouchableOpacity>
            </View>
            <View style={styles.gachaContainer}>
                <Image
                    source={jarImage}
                    style={styles.jarImage}
                />
                <Animated.Image
                    source={handImage}
                    style={[
                        // 固定スタイル
                        styles.handImage,
                        // 動的スタイル
                        {
                            transform: [
                                { translateY: pan.y }
                            ]
                        }
                    ]}
                    {...panResponder.panHandlers}
                />
            </View>
        </View>
    );
}

export default GachaButton

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#F8F0E3',
        paddingVertical: 0,
        position: 'relative',
    },
    tabContainer: {
        flexDirection: 'row',
        marginBottom: 30,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        borderRadius: 25,
        padding: 10,
        width: '90%',
        justifyContent: 'space-around',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
        borderWidth: 2,
        borderColor: 'rgba(255, 255, 255, 0.9)',
    },
    tab: {
        padding: 15,
        borderRadius: 20,
        marginHorizontal: 2,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        minWidth: 110,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(0, 0, 0, 0.1)',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    selectedTab: {
        backgroundColor: 'rgba(255, 236, 179, 0.9)',
        shadowColor: '#FFB74D',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.3,
        shadowRadius: 6,
        elevation: 6,
        transform: [{ scale: 1.05 }],
        borderWidth: 2,
        borderColor: '#FFB74D',
    },
    tabText: {
        fontSize: 16,
        fontWeight: '800',
        color: '#2C3E50',
        textShadowColor: 'rgba(0, 0, 0, 0.1)',
        textShadowOffset: { width: 1, height: 1 },
        textShadowRadius: 2,
    },
    gachaContainer: {
        position: 'relative',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: 600,
        marginTop: 20,
    },
    jarImage: {
        width: 420,
        height: 420,
        resizeMode: 'contain',
        position: 'absolute',
        bottom: 0,
        opacity: 1,
        backgroundColor: 'transparent',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.2,
        shadowRadius: 8,
        elevation: 5,
    },
    handImage: {
        position: 'absolute',
        width: 320,
        height: 320,
        resizeMode: 'contain',
        top: 120,
        opacity: 1,
        backgroundColor: 'transparent',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.2,
        shadowRadius: 8,
        elevation: 5,
    }
});