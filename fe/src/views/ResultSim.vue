<template>
  <div>
    <div class="resHeader">
      <img @click="goBack" src="../assets/imgs/back.png" alt="" /><span
        @click="goBack"
        class="back"    
        >返回</span
      ><span class="title">检测结果</span>
     
    </div>
     <!-- <div v-if="result">
          {{result}}
    </div> -->
    
    <div v-if="sim_res">
      <table>
        <thead>
          <th>FileType</th>
          <th>MachineType</th>
          <th>filesize</th>
          <th>md5</th>
          <th>time</th>
        </thead>
        <tbody>
          <tr v-for="res in sim_res" :key='res'>
            <td>{{res.FileType}}</td>
            <td>{{res.MachineType}}</td>
            <td>{{res.filesize}}</td>
            <td>{{res.md5}}</td>
            <td>{{res.time}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div vif="graph" ref="avgtime" :style="{ width: '100%', height: '1000px' }"></div>
    <div vif="graph" ref="avgtime1" :style="{ width: '500px', height: '500px' }"></div>
    <!-- <el-page-header @back="goBack" content="检测结果页面"> </el-page-header> -->
    <!-- <div v-if="result" class="results">
      <div class="words">
        <img :src="require(`../assets/imgs/${result.status}.png`)" alt="" />
       
        <div class="necessary">
          <div>md5:{{ result.md5 }}</div>
          <div>文件名称:{{ result.filename }}</div>
          <div>文件大小:{{ result.filesize | byteFormat }}</div>
          <div>上传者:{{ result.user }}</div>
        </div>
        <div class="unnecessry">
          <div>上传时间:{{ result.time | dateFormat }}</div>
          <div>总热度:{{ result.count }}</div>
          <div v-if="result.currentcount">
            当前热度:{{ result.currentcount }}
          </div>

          <div v-if="result.exist">exist:{{ result.exist }}</div>
          <div v-if="result.pe_time">petime:{{ result.pe_time }}</div>
          <div v-if="result.check_time">checktime:{{ result.check_time }}</div>
        </div>
      </div>

    </div> -->
  </div>
</template>

<script>
import Coff from "./details/Coff";
import Sections from "./details/Sections";
import Optional from "./details/Optional";
import Imports from "./details/Imports";

export default {
  //  async drawLine() {
  //   document.title = "结果";
  //   const { key } = this.$route.params;
  //   const { data } =  await this.$http.get(`/searchfilemd5/sim/${key}`);
  //   this.result = data;
  //   this.coff = data.coff || {};
  //   this.optional = data.optional || {};
  //   this.imports = data.imports || [];
  //   this.sections = data.sections || [];
  //   this.sim_res = data.sim_res || [];
  // },
  data() {
    return {
      result: {},
      activeName: "DOS头",
      coff: {},
      optional: {},
      imports: [],
      sections: [],
      sim_res:[],
      graph:{},
    };
  },
  async created(){
    document.title = "结果";
    const { key } = this.$route.params;
    const { data } =  await this.$http.get(`/searchfilemd5/sim/${key}`);
    this.result = data;
    this.graph = data.graph || {};
    this.coff = data.coff || {};
    this.optional = data.optional || {};
    this.imports = data.imports || [];
    this.sections = data.sections || [];
    this.sim_res = data.sim_res || [];
    // this.drawLine([1,2,3,4,5,6,7]);
    this.drawGraph(this.graph);

  },
  methods: {
    goBack() {
      this.$router.back(-1);
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    async drawLine(test){
    
    let mychart = this.$echarts.init(this.$refs.avgtime1);
    let option = {
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: test,
          type: 'line'
        }
      ]
      };
    mychart.setOption(option);
    },
    async drawGraph(graph){
        let myChart = this.$echarts.init(this.$refs.avgtime);
        let option = {
          tooltip: {},
          legend: [
            {
              data: graph.categories.map(function (a) {
                return a.name;
              })
            }
          ],
          series: [
            {
              name: 'Les Miserables',
              type: 'graph',
              layout: 'none',
              data: graph.nodes,
              links: graph.links,
              categories: graph.categories,
              roam: true,
              label: {
                show: true,
                position: 'right',
                formatter: '{b}'
              },
              labelLayout: {
                hideOverlap: true
              },
              scaleLimit: {
                min: 0.4,
                max: 2
              },
              lineStyle: {
                color: 'source',
                curveness: 0.3
              }
            }
          ]
        };
        myChart.setOption(option);
          },
  },
  components: {
    Coff,
    Sections,
    Optional,
    Imports,
  },
  mounted(){

    //this.drawGraph(this.graph)
    // this.$nextTick(()=>{
    //   this.drawLine()
    // })
  },
};





</script>

<style scoped>
.resHeader {
  position: relative;
  height: 50px;
  display: flex;
  align-items: center;
  box-shadow: rgb(17 17 17 / 16%) 0px 4px 8px -3px;
  margin-bottom: 15px;
}
.words {
  display: flex;
  justify-content: space-between;
}

.resHeader img {
  display: inline-block;
  width: 30px;
  height: 30px;
}

.resHeader img:hover,
.resHeader .back:hover {
  cursor: pointer;
}

.resHeader .back {
  /* margin: 20px 0; */
  /* padding: 5px; */
  position: relative;
}
.resHeader .back::after {
  content: "";
  position: absolute;
  width: 3px;
  height: 90%;
  background-color: #000;
  left: 45px;
  top: 50%;
  transform: translateY(-50%);
}

.title {
  position: absolute;
  font-size: 24px;
  left: 50%;
  transform: translateX(-50%);
}

.results {
  width: 86vw;
  margin: 0 auto;
  /* height: calc(100vh - 50px); */
  /* background-color: rgb(237, 240, 244); */
}
</style>
