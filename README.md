

# Smart Vehicle & Helmet Detection System

## Overview
This project is a real-time AI-based system to monitor vehicles at an entry gate.  
It detects vehicles, persons, helmets, and number plates, decides gate access, and logs events to a database.

## Features
- Live IP camera (RTSP) streaming
- Vehicle & person detection
- Helmet detection for two-wheelers
- Automatic number plate recognition (OCR)
- Gate decision (ALLOW / BLOCK)
- MySQL database logging
- Real-time web-based display

## Tech Stack
- Backend: Python, Flask
- AI Models: YOLOv8 (vehicle/person), custom YOLO (helmet & plate)
- OCR: EasyOCR
- Database: MySQL
- Streaming: HTTP MJPEG
- Camera: IP Camera (RTSP)

## Decision Logic
- Two-wheeler: Helmet + Number Plate → ALLOW
- Four-wheeler: Number Plate → ALLOW

## How to Run
1. Install dependencies
2. Configure RTSP camera URL
3. Start backend:



























# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
