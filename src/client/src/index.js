import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './styles/index.css';
import App from './components/App';
import MainRoot from './components/MainRoot';
import MainUrl from './components/MainUrl';
import MainPdf from './components/MainPdf';
import MainQuery from './components/MainQuery';
import ErrorPage from "./components/ErrorPage";
import reportWebVitals from './reportWebVitals';


const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <MainRoot />,
      },
      {
        path: "/url",
        element: <MainUrl/>,
      },
      {
        path: "/pdf",
        element: <MainPdf/>,
      },
      {
        path: "/query/:collectionId/:sourceName",
        element: <MainQuery/>,
      },
    ],
  },
]);


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
