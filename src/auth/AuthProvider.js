import {useContext, createContext, useState, useEffect} from 'react';


const AuthContext = createContext({
    isAuthenticated: false,
    getAccessToken: () => {},
    getRefreshToken: () => {},
    saveUser: () => {}
});

export function AuthProvider({children}) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [accessToken, setAccessToken] = useState();
    const [userInfo, setUserInfo] = useState();


    useEffect(() => {}, [])

    async function checkAuth() {
        if (accessToken) {
            // user is already logged in
        } else {
            // user is not logged in
            const token = getRefreshToken();
        }

    }
    
    
    function getAccessToken() {
        return accessToken;
    }

    function getRefreshToken() {
        const token = localStorage.getItem("token");
        return token ? JSON.parse(token) : null;
    }

    function saveUser(loginResponse) {
        setAccessToken(loginResponse.access_token);
        localStorage.setItem("token", loginResponse.access_token);
        setIsAuthenticated(true);
    }

    return (
    <AuthContext.Provider value={{isAuthenticated, getAccessToken, getRefreshToken, saveUser}}>
        {children}
    </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);