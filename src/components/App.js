import '../styles/App.css';
import Header from './Header';
import Footer from './Footer';
import { Outlet } from "react-router-dom";

function App() {
    return (
        <div id="app" className="App overflow-auto min-h-[900px] opacity-87 relative h-screen p-2 gap-2
		flex-col justify-center items-center m-auto flex text-white bg-[#161718] text-center">
			<div className="overflow-y-auto h-[100%] w-[70%] min-w-[1015px] p-2 gap-2 grid grid-cols-1 grid-rows-[1fr,5fr,1fr]">
				<header className="min-h-[100%] flex-col flex relative">
					<Header />
				</header>

				<main className="h-[100%] relative">
					<Outlet />
				</main>
				
				<footer className="min-h-[100%] relative">
					<Footer />
				</footer>
			</div>
		</div>
    );
}

export default App;
