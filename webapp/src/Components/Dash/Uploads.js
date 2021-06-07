import React from "react";
import Link from "@material-ui/core/Link";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Title from "./Title";
import axios from "axios";

function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles({
  depositContext: {
    flex: 1,
  },
});

export default function Uploads() {
  const classes = useStyles();
  const [file, setFile] = React.useState({ name: null, date: null});

  async function getLatest() {
    try {
      const { status, data, statusText } = await axios.get("/latest-file/", {
        params: {
          username: localStorage.getItem("username"),
        },
      });

      if (status === 200) {
        setFile(data[0]);
      }

      if (status === 401) {
        throw new Error(statusText);
      }
    } catch (e) {
      console.log(e);
      setFile({ name: null, date:null});
    }
  }

  React.useEffect(() => {
    getLatest();
  }, []);

  return (
    <React.Fragment>
      <Title>Latest Upload</Title>
      <Typography component="p" variant="h5">
        {file.name}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        {file.date}
      </Typography>
    </React.Fragment>
  );
}
