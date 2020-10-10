import * as React from 'react'
import { 
    createDrawerNavigator, 
    DrawerContentScrollView, 
    DrawerItem, 
    DrawerItemList, 
    useIsDrawerOpen 
} from '@react-navigation/drawer'
import * as SecureStore from 'expo-secure-store'
import { useFocusEffect } from '@react-navigation/native'
import Axios from 'axios'
import { SERVER_URI, AXIOS_HEADERS } from '../Constants/Network'
import { View, StyleSheet, Alert, BackHandler } from 'react-native'
import { ActivityIndicator, Avatar, Headline, Caption, ToggleButton, TouchableRipple } from 'react-native-paper'
import { MaterialCommunityIcons } from '@expo/vector-icons'
import UserTabNavigator from './UserTabNavigator'
import Profile from '../Screens/User/Drawer/Profile'
import Posts from '../Screens/User/Drawer/Posts'
import Likes from '../Screens/User/Drawer/Likes'
import Comments from '../Screens/User/Drawer/Comments'
import Goals from '../Screens/User/Drawer/Goals'

const DCS = (props) => {
    const [profile, setProfile] = React.useState({})
    const [loading, setLoading] = React.useState(true)
    const isDrawerOpen = useIsDrawerOpen()

    useFocusEffect(React.useCallback(() => {
        if (isDrawerOpen)
            getProfileData()
    },[useIsDrawerOpen]))

    const getProfileData = () => {
        setLoading(true)
        SecureStore.getItemAsync('token')
        .then(token => {
            return Axios.get(
                `${SERVER_URI}/user/profile/`,
                {
                    headers: {
                        ...AXIOS_HEADERS,
                        "Authorization": `Bearer ${token}`
                    }
                }
            )
        })
        .then(res => setProfile(res.data.data))
        .then(() => setLoading(false))
        .catch(err => {
            setLoading(false)
            alert(err.message)
        })
    }

    const handleLogOut = () => {
        SecureStore.deleteItemAsync('token')
        .then(() => props.navigation.navigate("Login"))
        .catch(console.log)
    }

    return(
        <DrawerContentScrollView {...props}>
            <View style={styles.dcsv}>
            {
                !loading ?
                <>
                    <Avatar.Text
                        size={64}
                        label={profile.user.first_name[0] + profile.user.last_name[0]}
                    />
                    <Headline style={styles.headLine}>
                        {profile.user.first_name + " " + profile.user.last_name}
                    </Headline>
                    <Caption>
                        {profile.user.gender + " | " + profile.user.age}
                    </Caption>
                    <Caption>
                        {profile.user.country}
                    </Caption>
                </>
                :
                <TouchableRipple onPress={getProfileData}>
                    <ActivityIndicator animating={true}/>
                </TouchableRipple>
            }
            </View>
            <DrawerItemList {...props}/>
            <DrawerItem
                label='Logout'
                onPress={handleLogOut}
                icon={({color}) => <MaterialCommunityIcons name='logout' color={color}/>}
            />
        </DrawerContentScrollView>
    )
}

const Drawer = createDrawerNavigator()

const DrawerItems = [
    {
        name: "Home",
        component: UserTabNavigator,
        iconName: 'home'
    },
    {
        name: "Profile",
        component: Profile,
        iconName: 'account'
    },
    {
        name: "Posts",
        component: Posts,
        iconName: 'file-document-box-multiple'
    },
    {
        name: "Likes",
        component: Likes,
        iconName: 'inbox-arrow-up'
    },
    {
        name: "Comments",
        component: Comments,
        iconName: 'comment-multiple'
    },
    {
        name: "Goals",
        component: Goals,
        iconName: 'format-list-numbered'
    }
]

export default ({ navigation }) => {

    useFocusEffect(React.useCallback(() => {
        const onBackPress = () => {
            Alert.alert(
                'Log out', 
                'Are you sure you want to log out?',
                [
                    {
                        text: 'CANCEL',
                        style: 'cancel',
                        onPress: () => {}
                    },
                    {
                        text: 'LOG OUT',
                        style: 'destructive',
                        onPress: handleLogOut
                    }
                ]
            )
            return true
        }

        BackHandler.addEventListener('hardwareBackPress', onBackPress)
        return () => BackHandler.removeEventListener('hardwareBackPress', onBackPress)
    }, []))

    const handleLogOut = () => {
        SecureStore.deleteItemAsync('token')
        .then(() => props.navigation.navigate("Login"))
        .catch(console.log)
    }

    return(
        <Drawer.Navigator initialRouteName="Home" drawerContent={props => <DCS {...props}/>}>
        {
            DrawerItems.map((item, index) =>
                <Drawer.Screen
                    key={index}
                    name={item.name}
                    component={item.component}
                    options={{
                        drawerIcon: ({color}) => <MaterialCommunityIcons name={item.iconName} color={color}/>
                    }}
                />
            )
        }
        </Drawer.Navigator>
    )
}

const styles = StyleSheet.create({
    dcsv: {
        height: 250,
        alignItems: 'center',
        justifyContent: 'center'
    },
    headLine: { marginTop: 15 }
})