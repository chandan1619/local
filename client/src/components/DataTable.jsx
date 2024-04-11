import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Modal from "react-modal";

const DataTable = ({ projects }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState("");

  const openModal = (filePath) => {
    setSelectedFile(`${process.env.REACT_APP_BACKEND_URL}${filePath}`); // Update the base URL as needed
    setModalIsOpen(true);
  };

  if (projects && projects.length == 0) return;

  return (
    <div className="flex flex-col">
      <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 sm:px-6 lg:px-8">
          <div className="overflow-hidden">
            <table className="min-w-full text-center text-sm font-light">
              <thead className="border-b bg-neutral-50 font-medium dark:border-neutral-500 dark:text-neutral-800">
                <tr>
                  <th scope="col" className=" px-6 py-4">
                    #
                  </th>
                  <th scope="col" className=" px-6 py-4">
                    Project Name
                  </th>
                  <th scope="col" className=" px-6 py-4">
                    Knowledge Base
                  </th>

                  {projects && projects[0] && projects[0].email && (
                    <th scope="col" className=" px-6 py-4">
                      Owner
                    </th>
                  )}
                  <th scope="col" className=" px-6 py-4">
                    Chat
                  </th>
                </tr>
              </thead>
              <tbody>
                {projects &&
                  projects.map((project, index) => (
                    <tr
                      key={index}
                      className="border-b dark:border-neutral-500"
                    >
                      <td className="whitespace-nowrap  px-6 py-4 font-medium">
                        {project.id}
                      </td>

                      <td className="whitespace-nowrap  px-6 py-4">
                        {project.name}
                      </td>

                      <td className="whitespace-nowrap  px-6 py-4">
                        {project.documents &&
                          project.documents.map((document, index) => (
                            <li
                              key={index}
                              className="list-none text-blue-500 hover:text-blue-700 font-medium hover:underline"
                              onClick={() =>
                                openModal(`/documents/${document.id}`)
                              }
                              style={{ cursor: "pointer" }}
                            >
                              {document.filename}
                            </li>
                          ))}
                      </td>
                      {project.email && (
                        <td className="whitespace-nowrap  px-6 py-4">
                          {project.email}
                        </td>
                      )}

                      <td className="whitespace-nowrap  px-6 py-4">
                        <Link
                          to={`/chat/${project.id}`}
                          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
                        >
                          Chat Now
                        </Link>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={() => setModalIsOpen(false)}
        contentLabel="Document Content"
      >
        <iframe
          title="Document Preview"
          src={selectedFile}
          width="100%"
          height="100%"
        />
      </Modal>
    </div>
  );
};

export default DataTable;
