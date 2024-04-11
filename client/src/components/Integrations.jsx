import React, { useState, useEffect, useRef } from "react";
import Jira from "../components/Jira";
import Slack from "../components/Slack";
import Discord from "../components/Discord";
import Github from "../components/Github";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const Integrations = () => {
  const comp = useRef("initial");
  const navigate = useNavigate();
  const user = useSelector((state) => state.user.value);

  const fetchSlacktoken = async () => {
    console.log("fetching slack code");
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code"); // Assuming the parameter name is 'token'
    if (code) {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/slacklogin/redirect?code=${code}&user_id=${user?.id}`,
          {
            method: "GET",
          }
        );

        const data = await response.json();

        // Dispatching user data to Redux stor
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    }
  };

  const fetchGithubktoken = async () => {
    console.log("fetching github code");
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code"); // Assuming the parameter name is 'token'
    if (code) {
      try {
        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/githublogin/redirect?code=${code}&user_id=${user?.id}`,
          {
            method: "GET",
          }
        );

        const data = await response.json();

        // Dispatching user data to Redux stor
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    }
  };

  return (
    <>
      <Jira />
      <Slack fetchSlacktoken={fetchSlacktoken} />
      <Discord />
      <Github fetchGithubktoken={fetchGithubktoken} />
    </>
  );
};

export default Integrations;
