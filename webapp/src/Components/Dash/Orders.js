import React from "react";
import Link from "@material-ui/core/Link";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Title from "./Title";
import axios from "axios";

async function createData(filename) {
  try {
    const { status, data, statusText } = await axios.get("/file-get-report/", {
      data: {
        filename,
      },
    });

    if (status === 200) {
      const { name, compressedSize, uncompressedSize, isBomb } = data;
      return { name, compressedSize, uncompressedSize, isBomb };
    }

    if (status === 401) {
      throw new Error(statusText);
    }
  } catch (e) {
    console.log(e);
    return { name:filename, compressedSize:0, uncompressedSize:0, isBomb:0 }
  }
}

async function getFiles() {
  try {
    const { status, data, statusText } = await axios.get("/user-file-list/");

    if (status === 200) {
      let rows = [];
      let i = 0;
      data.files.forEach((filename) => {
        let row =  createData(filename)
        row["id"] = i;
        rows.push(row);
        i++;
      });
      return rows;
    }

    if (status === 401) {
      throw new Error(statusText);
    }
  } catch (e) {
    console.log(e);
    return []
  }
}


function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles((theme) => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
}));

export default function Orders() {
  const classes = useStyles();
  const rows = getFiles();
  return (
    <React.Fragment>
      <Title>Recent Orders</Title>
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
        <Link color="primary" href="#" onClick={preventDefault}>
          See more orders
        </Link>
      </div>
    </React.Fragment>
  );
}
