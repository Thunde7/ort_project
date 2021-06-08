import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import axios from 'axios';

export default function Chart() {
  const theme = useTheme();
  const [data, setData] = React.useState([])

  async function getFiles() {
    try {
      const { status, data, statusText } = await axios.get("/file-data-list/", {
        headers: {
          Auth : localStorage.getItem("token")
        },
        params: {
          username: localStorage.getItem("username"),
        },
      });

      if (status === 200) {
        let files = data.files.map(file => file.metadata)
        setData(files)
      }

      if (status === 401) {
        throw new Error(statusText);
      }
    } catch (e) {
      console.log(e);
      setData([]);
    }
  }

  React.useEffect(() => {
    getFiles();
  }, [])

  return (
    <React.Fragment>
      <Title>Your File Trend</Title>
      <ResponsiveContainer>
        <LineChart
          data={data}
          margin={{
            top: 16,
            right: 16,
            bottom: 0,
            left: 24,
          }}
        >
          <XAxis dataKey="name" stroke={theme.palette.text.secondary} />
          <YAxis dataKey="ratio" stroke={theme.palette.text.secondary}>
            <Label
              angle={270}
              position="left"
              style={{ textAnchor: 'middle', fill: theme.palette.text.primary }}
            >
              Ratio 
            </Label>
          </YAxis>
          <Line type="monotone" dataKey="amount" stroke={theme.palette.primary.main} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
