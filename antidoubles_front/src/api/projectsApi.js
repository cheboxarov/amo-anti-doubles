import { BASE_URL, TOKEN } from "../config";

const API_BASE_URL = `${BASE_URL}/projects`;

const headers = {
    Authorization: `Bearer ${TOKEN}`,
    'Content-Type': 'application/json',
};

export const getAllProjects = async () => {
  const response = await fetch(API_BASE_URL, {
    headers
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const getProjectById = async (projectId) => {
  const response = await fetch(`${API_BASE_URL}/${projectId}`, {
    headers
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const createProject = async (projectData) => {
  const response = await fetch(API_BASE_URL, {
    method: 'POST',
    headers,
    body: JSON.stringify(projectData),
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const updateProject = async (projectId, projectData) => {
  const response = await fetch(`${API_BASE_URL}/${projectId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(projectData),
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const deleteProject = async (projectId) => {
  const response = await fetch(`${API_BASE_URL}/${projectId}`, {
    method: 'DELETE',
    headers,
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return true;
};
