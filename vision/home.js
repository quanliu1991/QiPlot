import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Upload, FileText, MessageCircle, BarChart2 } from "lucide-react";

export default function AIPlotApp() {
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);
  const [outputImage, setOutputImage] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleGenerate = () => {
    // TODO: 发送数据到后端，生成学术图表
    console.log("描述:", description, "文件:", file);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-4">
      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="flex items-center space-x-2">
            <MessageCircle className="text-blue-500" />
            <h2 className="text-lg font-semibold">对话窗口</h2>
          </div>
          <Textarea
            placeholder="请输入实验数据的描述，例如‘绘制柱状图，x 轴为时间，y 轴为实验测量值’"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="flex items-center space-x-2">
            <Upload className="text-green-500" />
            <h2 className="text-lg font-semibold">上传实验数据</h2>
          </div>
          <Input type="file" onChange={handleFileChange} />
        </CardContent>
      </Card>

      <Button onClick={handleGenerate} className="w-full bg-blue-600 hover:bg-blue-700">
        生成图表
      </Button>

      {outputImage && (
        <Card>
          <CardContent className="p-4 space-y-4">
            <div className="flex items-center space-x-2">
              <BarChart2 className="text-purple-500" />
              <h2 className="text-lg font-semibold">生成的学术图表</h2>
            </div>
            <img src={outputImage} alt="生成的学术图表" className="w-full" />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
