import { useEffect, useState } from "react";
import Header from "../components/Header";
import ProjectCreate from "../components/ProjectCreate";
import DataTable from "../components/DataTable";
import Integrations from "../components/Integrations";

import { Link } from "react-router-dom";
import Toast from "../components/Toast";
import { toast } from "react-toastify";

import { useSelector } from "react-redux";

function Home() {
  const user = useSelector((state) => state.user.value);
  const [projects, setProjects] = useState([]); // The empty array ensures this effect runs only once after the initial render
  useEffect(() => {
    fetchProjects();
  }, []); // The empty array ensures this effect runs only once after the initial render
  const fetchProjects = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/projects?id=${user.id}`
    ); // Adjust the URL/port as necessary
    const data = await response.json();
    setProjects(data);
  };

  const handleDataPull = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/fetch-data?user_id=${user.id}`
    );

    const data = await response.json();

    if (response.status == 200) {
      toast(<Toast message={data} type="success" />);
    } else {
      toast(<Toast message="Error fetching data" type="error" />);
    }
  };

  return (
    <div className="">
      <Header />
      <div className="flex flex-row gap-4 m-10  items-center flex-wrap">
        <Integrations/>
        <div className="flex flex-row items-center w-screen justify-around">
          <ProjectCreate projectupdate={fetchProjects} />
          <button
            onClick={handleDataPull}
            class="mt-4 flex items-center gap-x-2 justify-center rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700"
          >
            <p>Pull Data</p>

            <svg
              id="Layer_1_1_"
              enableBackground="new 0 0 64 64"
              height="30"
              viewBox="0 0 64 64"
              width="30"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="m27 12h10v2h-10z" />
              <path d="m27 16h10v2h-10z" />
              <path d="m57 54v-8c0-.444-.293-.835-.72-.96l-23.28-6.79v-12.25h7c.553 0 1-.448 1-1v-16c0-.265-.105-.52-.293-.707l-6-6c-.187-.188-.441-.293-.707-.293h-10c-.553 0-1 .448-1 1v22c0 .552.447 1 1 1h7v12.25l-23.28 6.79c-.427.125-.72.516-.72.96v8c0 .444.293.835.72.96l24 7c.092.027.185.04.28.04s.188-.013.28-.04l24-7c.427-.125.72-.516.72-.96zm-22-48.586 2.586 2.586h-2.586zm-10-1.414h8v5c0 .552.447 1 1 1h5v14h-14zm6 36.333v5.253l-2.293-2.293-1.414 1.414 4 4c.195.195.451.293.707.293s.512-.098.707-.293l4-4-1.414-1.414-2.293 2.293v-5.253l19.429 5.667-20.429 5.958-20.429-5.958zm-22 7 22 6.417v5.917l-22-6.417zm24 12.334v-5.917l22-6.417v5.917z" />
              <path d="m27 8h4v2h-4z" />
              <path d="m3 26h7c0 2.757 2.243 5 5 5h3c1.654 0 3 1.346 3 3v1.586l-2.293-2.293-1.414 1.414 4 4c.195.195.451.293.707.293s.512-.098.707-.293l4-4-1.414-1.414-2.293 2.293v-1.586c0-2.757-2.243-5-5-5h-3c-1.654 0-3-1.346-3-3h7c.553 0 1-.448 1-1v-16c0-.265-.105-.52-.293-.707l-6-6c-.187-.188-.441-.293-.707-.293h-10c-.553 0-1 .448-1 1v22c0 .552.447 1 1 1zm11-20.586 2.586 2.586h-2.586zm-10-1.414h8v5c0 .552.447 1 1 1h5v14h-14z" />
              <path d="m6 12h10v2h-10z" />
              <path d="m6 16h10v2h-10z" />
              <path d="m6 20h10v2h-10z" />
              <path d="m6 8h4v2h-4z" />
              <path d="m62 25v-16c0-.265-.105-.52-.293-.707l-6-6c-.187-.188-.441-.293-.707-.293h-10c-.553 0-1 .448-1 1v22c0 .552.447 1 1 1h7c0 1.654-1.346 3-3 3h-3c-2.757 0-5 2.243-5 5v1.586l-2.293-2.293-1.414 1.414 4 4c.195.195.451.293.707.293s.512-.098.707-.293l4-4-1.414-1.414-2.293 2.293v-1.586c0-1.654 1.346-3 3-3h3c2.757 0 5-2.243 5-5h7c.553 0 1-.448 1-1zm-6-19.586 2.586 2.586h-2.586zm-10 18.586v-20h8v5c0 .552.447 1 1 1h5v14z" />
              <path d="m48 12h10v2h-10z" />
              <path d="m48 16h10v2h-10z" />
              <path d="m48 20h10v2h-10z" />
              <path d="m48 8h4v2h-4z" />
              <path d="m27 20h2v2h-2z" />
              <path d="m31 20h2v2h-2z" />
              <path d="m35 20h2v2h-2z" />
            </svg>
          </button>
          <Link
            to={`/chat/integrations`}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
          >
            Chat With Integrations
          </Link>
        </div>
      </div>
      <div className="p-8">
        <DataTable projects={projects} />
      </div>
    </div>
  );
}

export default Home;
