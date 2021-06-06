import React, { useCallback } from "react";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import DashboardIcon from "@material-ui/icons/Dashboard";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import PublishIcon from "@material-ui/icons/Publish";

import axios from "axios";
import { useHistory } from "react-router-dom";
import { useSetRecoilState } from "recoil";
import { tokenState } from "../atoms";
import { useFormik } from 'formik';
import * as Yup from "yup";
import { Button } from "@material-ui/core";

const uploadDefaults = {
  filename: "",
  file: "",
}

const UploadScheme = () =>
  Yup.object().shape({
    filename: Yup.string().required("Username can't be empty"),
    file: Yup.string().required("password can't be empty"),
  });

export default function SideBar() {
  const history = useHistory();
  const setToken = useSetRecoilState(tokenState);

  const redirectToDash = useCallback(() => {
    history.push("/dashboard")
  })

  const redirectToHome = useCallback(() => {
    console.log("logged out");
    history.push("/login");
  }, []);

  const deleteJWT = useCallback(() => {
    localStorage.setItem("token", null);
    axios.defaults.headers["Auth"] = null;
    setToken(null);
    redirectToHome();
  }, []);

  const onSubmit = (async (values) => {
    try {
      console.log(values);
    } catch(e) {
      console.error(e)
    }
  })

  const formik = useFormik({
    validationSchema: UploadScheme,
    initialValues: uploadDefaults,
    onSubmit,
  })

  return (
    <List>
      <ListItem button onClick={redirectToDash}>
        <ListItemIcon>
          <DashboardIcon />
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItem>
      <ListItem form onSubmit={formik.handleSubmit}>
        <ListItemIcon>
          <PublishIcon />
        </ListItemIcon>
        <Button
        type="submit"
        component="label">
        Upload
        <input
        type="file"
        hidden
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
