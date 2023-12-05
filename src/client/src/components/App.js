import '../styles/App.css';
import Header from './Header';

function App() {
    return (
        <div className="App overflow-auto max-h-[100vh] opacity-87 relative h-screen p-2 gap-2 border-2 border-white">
			<div className="h-[100%] gap-2 grid grid-cols-1 grid-rows-[1fr,5fr,1fr]">
				<header className="overflow-auto min-h-[100%] flex-col flex relative border-2 border-white">
					<Header />
				</header>

				<main className="overflow-auto h-[100%] relative border-2 border-white">
					main
				</main>
				
				<footer className="overflow-auto min-h-[100%] relative border-2 border-white">
					footer
				</footer>
			</div>
		</div>
    );
}

export default App;
