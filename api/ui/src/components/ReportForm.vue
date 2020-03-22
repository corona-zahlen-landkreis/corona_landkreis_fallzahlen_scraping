<template>
    <el-dialog :title="title" :visible.sync="show" append-to-body @close="close">
        <el-row>
            <el-col class="form-label" :span="10">Gemeinde/Landkreis</el-col>
            <el-col :span="14">
                <el-autocomplete
                    style="width: 100%"
                    v-model="location"
                    :fetch-suggestions="querySearch"
                    placeholder="Gemeinde/Landkreis wählen"
                    @select="handleSelect"
                ></el-autocomplete>
            </el-col>
        </el-row>
        <el-row>
            <el-col class="form-label" :span="10">Infiziert</el-col>
            <el-col :span="14">
                <el-input-number :min="0" v-model="infected" />
            </el-col>
        </el-row>
        <el-row>
            <el-col class="form-label" :span="10">Geheilt</el-col>
            <el-col :span="14">
                <el-input-number :min="0" v-model="cured" />
            </el-col>
        </el-row>
        <el-row>
            <el-col class="form-label" :span="10">Tot</el-col>
            <el-col :span="14">
                <el-input-number :min="0" v-model="dead" />
            </el-col>
        </el-row>
        <span slot="footer" class="dialog-footer">
            <el-button @click="close">Abbrechen</el-button>
            <el-button type="primary" @click="save">Einreichen</el-button>
        </span>
    </el-dialog>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
    name: "ReportForm",
    watch: {
        show() {
            if (!this.show) {
                this.close();
            }
        },
    },
    data() {
        return {
            title: "Neue Meldung",
            show: true,
            location: null,
            community_id: null,
            infected: 0,
            cured: 0,
            dead: 0,
        }
    },
    methods: {
        close() {
            this.$emit('pp-close');
        },
        async save() {
            let params = {
                report_date: moment(new Date()).format("YYYY-MM-DD"),
                community_id: this.community_id,
                infected: this.infected,
                cured: this.cured,
                dead: this.dead
            }

            try {
                if (!params.community_id) {
                    throw new Error("Bitte Gemeinde/Landkreis wählen");
                }


                let {status, data} = await axios.post(this.backendEndpoint + 'api/reports', params);
                if (status === 200) {
                    this.$emit('data-update', data);
                    this.close();
                } else {
                    throw new Error("Fehler beim anlegen der Meldung")
                }

            } catch (err) {
                this.$notify({
                    type: 'error',
                    title: 'Fehler',
                    message: err.message
                });
                return;
            }


        },
        async querySearch(queryString, cb) {
            try {
                let endPoint = this.backendEndpoint + 'api/locations';
                if (queryString) {
                    endPoint += '?q=' + encodeURIComponent(queryString)
                }
                let {status, data} = await axios.get(endPoint);
                if (status !== 200) {
                    cb([]);
                    return;
                }

                for (let location of data) {
                    location.value = `${location.type} ${location.community} (${location.state})`;
                }

                cb(data);
            } catch (err) {
                console.log(err);
                cb([]);
            }
        },
        handleSelect(item) {
            this.community_id = item.community_id;
        }
    }
};
</script>

<style lang="scss" scoped>
    .el-dialog .el-row {
        margin: 15px;

        .form-label {
            padding: 15px;
        }
    }
</style>
