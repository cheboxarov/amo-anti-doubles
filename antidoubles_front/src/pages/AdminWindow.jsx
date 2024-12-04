import React, { useEffect, useState } from "react";
import {
  getAllProjects,
  createProject,
  updateProject,
  deleteProject
} from "../api/projectsApi";
import {
  getAllWidgets,
  createWidget,
  updateWidget,
  deleteWidget
} from "../api/widgetsApi";
import styles from "./AdminWindow.module.css";
import { winState, WIN_STATES } from "../signals/pageStateSignals";

const AdminWindow = () => {
  const [projects, setProjects] = useState([]);
  const [widgets, setWidgets] = useState([]);
  const [newProject, setNewProject] = useState({
    subdomain: "",
    is_active: true,
    is_admin: false,
    widget_id: 0,
    unactive_reason: null,
    access_token: "",
    refresh_token: ""
  });
  const [newWidget, setNewWidget] = useState({
    client_id: "",
    secret_key: ""
  });

  useEffect(() => {
    Promise.all([fetchProjects(), fetchWidgets()]);
  }, []);

  const fetchProjects = async () => {
    try {
      const data = await getAllProjects();
      setProjects(data);
    } catch (error) {
      console.log("error to fetch projects", error);
    }
  };

  const fetchWidgets = async () => {
    try {
      const data = await getAllWidgets();
      setWidgets(data);
    } catch (error) {
      console.log("error to fetch widgets", error);
    }
  };

  const handleCreateProject = async () => {
    try {
      await createProject(newProject);
      fetchProjects();
      setNewProject({
        subdomain: "",
        is_active: true,
        is_admin: false,
        widget_id: 0,
        unactive_reason: null,
        access_token: "",
        refresh_token: ""
      });
    } catch (error) {
      console.log("error to create project", error);
    }
  };

  const handleCreateWidget = async () => {
    try {
      await createWidget(newWidget);
      fetchWidgets();
      setNewWidget({
        client_id: "",
        secret_key: ""
      });
    } catch (error) {
      console.log("error to create widget", error);
    }
  };

  const handleDeleteWidget = async (widgetId) => {
    try {
        await deleteWidget(widgetId)
        fetchWidgets()
    } catch (error) {
        console.log("error to delete widget", error)
    }
  }
  
  const handleDeleteProject = async (projectId) => {
    try {
        await deleteProject(projectId)
        fetchProjects()
    } catch (error) {
        console.log("error to delete project", error)
    }
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.header} onClick={() => { winState.value = WIN_STATES.DOUBLES }}>Админ-панель</h1>

      <section className={styles.section}>
        <h2>Проекты</h2>
        <ul className={styles.list}>
          {projects.map((project) => (
            <li key={project.id} className={styles.item}>
              {project.subdomain} ({project.is_active ? "Активен" : "Неактивен"})
              <button onClick={() => handleDeleteProject(project.id)} className={styles.button}>
                Удалить
              </button>
            </li>
          ))}
        </ul>
        <div className={styles.form}>
          <input
            type="text"
            placeholder="Subdomain"
            value={newProject.subdomain}
            onChange={(e) => setNewProject({ ...newProject, subdomain: e.target.value })}
            className={styles.input}
          />
          <input
            type="number"
            placeholder="Widget ID"
            value={newProject.widget_id}
            onChange={(e) => setNewProject({ ...newProject, widget_id: e.target.value })}
            className={styles.input}
          />
          <input
            type="text"
            placeholder="Access Token"
            value={newProject.access_token}
            onChange={(e) => setNewProject({ ...newProject, access_token: e.target.value })}
            className={styles.input}
          />
          <input
            type="text"
            placeholder="Refresh Token"
            value={newProject.refresh_token}
            onChange={(e) => setNewProject({ ...newProject, refresh_token: e.target.value })}
            className={styles.input}
          />
          <button onClick={handleCreateProject} className={styles.button}>
            Добавить проект
          </button>
        </div>
      </section>

      <section className={styles.section}>
        <h2>Виджеты</h2>
        <ul className={styles.list}>
          {widgets.map((widget) => (
            <li key={widget.id} className={styles.item}>
              {widget.client_id}:{widget.secret_key} ID:{widget.id}
              <button onClick={() => handleDeleteWidget(widget.id)} className={styles.button}>
                Удалить
              </button>
            </li>
          ))}
        </ul>
        <div className={styles.form}>
          <input
            type="text"
            placeholder="Client ID"
            value={newWidget.client_id}
            onChange={(e) => setNewWidget({ ...newWidget, client_id: e.target.value })}
            className={styles.input}
          />
          <input
            type="text"
            placeholder="Secret Key"
            value={newWidget.secret_key}
            onChange={(e) => setNewWidget({ ...newWidget, secret_key: e.target.value })}
            className={styles.input}
          />
          <button onClick={handleCreateWidget} className={styles.button}>
            Добавить виджет
          </button>
        </div>
      </section>
    </div>
  );
};

export default AdminWindow;
