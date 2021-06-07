import React, { useEffect } from "react";
import Link from "@material-ui/core/Link";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Title from "./Title";
import axios from "axios";

const useStyles = makeStyles((theme) => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
}));

export default function Files() {
  const classes = useStyles();
  const [rows, setRows] = React.useState([]);

  async function getFiles() {
    try {
      const { status, data, statusText } = await axios.get("/file-data-list/", {
        params: {
          username: localStorage.getItem("username"),
        },
      });

      if (status === 200) {
        console.log(data.files);

        let files = data.files.map(file => file.metadata)
        setRows(files)
      }

      if (status === 401) {
        throw new Error(statusText);
      }
    } catch (e) {
      console.log(e);
      setRows([]);
    }
  }

  React.useEffect(() => {
    getFiles();
  }, [])

  return (
    <React.Fragment>
      <Title>Recent Files</Title>
      <Table CompressedSize="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Compressed Size</TableCell>
            <TableCell>Uncompressed Size</TableCell>
            <TableCell align="right">Zip Bomb?</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.name}</TableCell>
              <TableCell>{row.compressedSize}</TableCell>
              <TableCell>{row.uncompressedSize}</TableCell>
              <TableCell align="right">{row.isBomb}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className={classes.seeMore}>
        <Link color="primary" href="#" onClick={getFiles}>
          See more files
        </Link>
      </div>
    </React.Fragment>
  );
}
