function DropdownMenu() {
  function handleClickAbout() {
    console.log("Redirecting to About page...");
  }

  function handleClickTutorial() {
    console.log("Redirecting to Tutorial page...");
  }

  return (
    <div className="rounded-bl-lg z-10 bg-zinc-900 shadow-md transition-all duration-300 linear">
      <ul>
        <li onClick={handleClickAbout} className="text-white hover:cursor-pointer hover:bg-zinc-800 transition-all duration-300 linear">About</li>
        <li onClick={handleClickTutorial} className="text-white rounded-bl-lg hover:cursor-pointer hover:bg-zinc-800 transition-all duration-300 linear">Tutorial</li>
      </ul>
    </div>
  );
};

export default DropdownMenu;