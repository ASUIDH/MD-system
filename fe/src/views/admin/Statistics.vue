<template>
  <div class="charts">
    <Size />
    <UploadNum />
    <AvgTime />
  </div>
</template>

<script>
import Size from "./charts/Size";
import UploadNum from "./charts/UploadNum";
import AvgTime from "./charts/AvgTime";

export default {
  name: "hello",
  components: {
    Size,
    UploadNum,
    AvgTime,
  },
};
</script>

<style scoped>
.charts {
  margin: 0 auto;
  width: 1000px;

  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
