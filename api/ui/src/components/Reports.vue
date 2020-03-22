<template>
    <div>
        <div class="headline">
            <h1>Meldungen</h1>
            <el-button @click="form.display = true">Neue Meldung</el-button>
        </div>
        <div>
             <el-table
                :data="reports"
                style="width: 100%"
                empty-text="Keine Meldungen"
                >
                <el-table-column
                    prop="report_date"
                    label="Gemeldet am"
                    width="180">
                </el-table-column>
                <el-table-column
                    prop="community"
                    label="Gemeinde/Landkreis"
                    width="380">
                </el-table-column>
                <el-table-column
                    prop="community_id"
                    label="Schlüssel"
                    width="380">
                </el-table-column>
                <el-table-column
                    prop="infected"
                    label="Infiziert">
                </el-table-column>
                <el-table-column
                    prop="cured"
                    label="Geheilt">
                </el-table-column>
                <el-table-column
                    prop="dead"
                    label="Tot">
                </el-table-column>
            </el-table>
            <ReportForm
                v-if="form.display"
                @pp-close="form.display = false"
                @data-update="load()"
            />
        </div>
    </div>
</template>

<script>

import axios from 'axios';
import ReportForm from './ReportForm';

export default {
    components: {
        ReportForm
    },
    name: "Reports",
    data() {
        return {
            form: {
                display: false,
            },
            reports: [],
        };
    },
    created() {
        // console.log(this.$route.params.id)

        this.load();
    },
    methods: {
        async load() {
            try {
                this.reports = [];

                let {status, data} = await axios.get(this.backendEndpoint + 'api/reports');
                if (status !== 200) {
                    this.$notify({
                        type: 'error',
                        title: 'Fehler',
                        message: 'Fehler beim laden der Daten'
                    });
                    return;
                }

                this.reports = data || [];
            } catch (err) {
                console.log(err);
            }
        }
    }
};
</script>

<style lang="scss" scoped>
    .headline {
        margin: 50px 0 0;
        padding: 50px;
    }
</style>
