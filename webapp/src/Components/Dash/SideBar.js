import React, { useCallback } from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import DashboardIcon from "@material-ui/icons/Dashboard";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import PublishIcon from "@material-ui/icons/Publish";
import AttachmentIcon from "@material-ui/icons/Attachment";

import axios from "axios";
import { useHistory } from "react-router-dom";
import { useFormik } from "formik";
import * as Yup from "yup";
import { Button, Typography } from "@material-ui/core";

const uploadDefaults = {
  file: "",
};

const UploadScheme = () =>
  Yup.object().shape({
    file: Yup.string().required("file can't be null"),
  });

export default function SideBar() {
  const history = useHistory();

  const redirectToDash = useCallback(() => {
    history.push("/dashboard");
  });

  const redirectToHome = useCallback(() => {
    console.log("logged out");
    history.push("/login");
  }, []);

  const deleteJWT = useCallback(() => {
    localStorage.setItem("token", null);
    localStorage.removeItem("username");
    redirectToHome();
  }, []);

  const toBase64 = async (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });

  const onSubmit = async (values) => {
    try {
      console.log(localStorage.getItem("token"));
      const { name } = values.file;
      const b64 = await toBase64(values.file);
      const { status, statusCode, data } = await axios.post(
        "/file-upload/",
        {
          data: {
            username: localStorage.getItem("username"),
            filename: name,
            file: b64,
          },
        },
        {
          headers: {
            Auth: localStorage.getItem("token"),
          },
        }
      );
    } catch (e) {
      console.error(e);
    }
  };

  const formik = useFormik({
    validationSchema: UploadScheme,
    initialValues: uploadDefaults,
    onSubmit,
  });

  return (
    <List>
      <ListItem button onClick={redirectToDash}>
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItem>
      <ListItem button onClick={formik.handleSubmit}>
        <ListItemIcon>
          <PublishIcon />
        </ListItemIcon>
        <ListItemText primary="Upload" />
      </ListItem>
      <ListItem>
        <Button type="submit" component="label">
          <ListItemIcon>
            <AttachmentIcon />
          </ListItemIcon>
          <ListItemText
            primary={
              !!formik.values.file ? formik.values.file.name : "Choose file"
            }
          />
          <input
            type="file"
            hidden
            onChange={(e) => {
              formik.setFieldTouched("file");
              formik.setFieldValue("file", e.currentTarget.files[0]);
            }}
          />
        </Button>
      </ListItem>
      <ListItem button onClick={deleteJWT}>
        <ListItemIcon>
          <ExitToAppIcon />
        </ListItemIcon>
        <ListItemText primary="Logout" />
      </ListItem>
    </List>
  );
}
