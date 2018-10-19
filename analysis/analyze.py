import csv
import matplotlib.pyplot as plt
from attrdict import AttrDict

def analyze_fhe_vs_rsa_dual(params):
    rsa_y1_data = []
    fhe_y1_data = []
    rsa_y2_data = []
    fhe_y2_data = []
    rsa_x_data = []
    fhe_x_data = []

    with open(params.ref_csv_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            should_skip = False
            for condition in params.constants:
                if str(row[condition.name]) != str(condition.val):
                    should_skip = True
                    break
            
            if should_skip: continue

            if row['enc_mode'] == 'RSA':
                rsa_x_data.append(float(row[params.x_axis]))
                rsa_y1_data.append(float(row[params.y1_axis]))
                rsa_y2_data.append(float(row[params.y2_axis]))

            elif row['enc_mode'] == 'FHE':
                fhe_x_data.append(float(row[params.x_axis]))
                fhe_y1_data.append(float(row[params.y1_axis]))
                fhe_y2_data.append(float(row[params.y2_axis]))

    plt.figure(params.name)

    line_1, = plt.plot(rsa_x_data, rsa_y1_data, params.line_1_fmt, label=params.line_1_lbl)
    line_2, = plt.plot(fhe_x_data, fhe_y1_data, params.line_2_fmt, label=params.line_2_lbl)
    line_3, = plt.plot(rsa_x_data, rsa_y2_data, params.line_3_fmt, label=params.line_3_lbl)
    line_4, = plt.plot(fhe_x_data, fhe_y2_data, params.line_4_fmt, label=params.line_4_lbl)

    plt.legend(handles=[line_1, line_2, line_3, line_4])
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.ylabel(params.y_axis_lbl)
    plt.xlabel(params.x_axis_lbl)

    plt.suptitle(params.desc)

    plt.show()

    return


def analyze_fhe_vs_rsa(params):
    rsa_y_data = []
    fhe_y_data = []
    rsa_x_data = []
    fhe_x_data = []

    with open(params.ref_csv_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            should_skip = False
            for condition in params.constants:
                if str(row[condition.name]) != str(condition.val):
                    should_skip = True
                    break
            
            if should_skip: continue

            if row['enc_mode'] == 'RSA':
                rsa_x_data.append(float(row[params.x_axis]))
                rsa_y_data.append(float(row[params.y_axis]))

            elif row['enc_mode'] == 'FHE':
                fhe_x_data.append(float(row[params.x_axis]))
                fhe_y_data.append(float(row[params.y_axis]))

    plt.figure(params.name)

    line_1, = plt.plot(rsa_x_data, rsa_y_data, params.line_1_fmt, label=params.line_1_lbl)
    line_2, = plt.plot(fhe_x_data, fhe_y_data, params.line_2_fmt, label=params.line_2_lbl)

    plt.legend(handles=[line_1, line_2])
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.ylabel(params.y_axis_lbl)
    plt.xlabel(params.x_axis_lbl)

    plt.suptitle(params.desc)

    plt.show()

    return

def analyze_single(params):
    y_data = []
    x_data = []

    with open(params.ref_csv_file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            should_skip = False
            for condition in params.constants:
                if str(row[condition.name]) != str(condition.val):
                    should_skip = True
                    break
            
            if should_skip: continue

            x_data.append(float(row[params.x_axis]))
            y_data.append(float(row[params.y_axis]))

    plt.figure(params.name)

    line_1, = plt.plot(x_data, y_data, params.line_1_fmt, label=params.line_1_lbl)

    plt.legend(handles=[line_1])
    plt.ylim(bottom=0, top=(max(y_data)*1.5))
    plt.xlim(left=0)
    plt.ylabel(params.y_axis_lbl)
    plt.xlabel(params.x_axis_lbl)

    plt.suptitle(params.desc)

    plt.show()

    return


def analyze():
    analysis_tbl = [
            AttrDict({ 
                "name" : "Figure 1 OT vs MBS",
                "desc" : "Overall Time vs Max Tx/Rx Buffer Size",
                "constants" : [{ "name" : "data_size", "val" : 500 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "max_buf_size",
                "x_axis_lbl" : "Max Tx/Rx Buffer Size",
                "y_axis" : "overall",
                "y_axis_lbl" : "Overall Time",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 2 OT vs DS",
                "desc" : "Overall Time vs Data Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "overall",
                "y_axis_lbl" : "Overall Time",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 3 EDT vs DS",
                "desc" : "Encrypt/Decrypt Time vs Data Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "x_axis_fmt" : "r-",
                "y1_axis" : "encrypt",
                "y2_axis" : "decrypt",
                "y_axis_lbl" : "Encrypt/Decrypt Time",
                "line_1_lbl" : "Encrypt RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "Decrypt RSA",
                "line_2_fmt" : "b-",
                "line_3_lbl" : "Encrypt FHE",
                "line_3_fmt" : "m-",
                "line_4_lbl" : "Decrypt FHE",
                "line_4_fmt" : "g-",
                "perform" : analyze_fhe_vs_rsa_dual }),

            AttrDict({ 
                "name" : "Figure 4 TxT vs MBS",
                "desc" : "Transmit Time vs Max Tx/Rx Buffer Size",
                "constants" : [{ "name" : "data_size", "val" : 500 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "max_buf_size",
                "x_axis_lbl" : "Max Tx/Rx Buffer Size",
                "y_axis" : "transmit",
                "y_axis_lbl" : "Transmit Time",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 5 TxT vs DS",
                "desc" : "Transmit Time vs Data Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "transmit",
                "y_axis_lbl" : "Transmit Time",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 6 EvT vs DS",
                "desc" : "Evaluation Time vs Data Size",
                "constants" : [ { "name" : "max_buf_size", "val" : 4096 },
                                { "name" : "enc_mode", "val" : "FHE" }],
                "ref_csv_file" : "node_server.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "evaluate",
                "y_axis_lbl" : "Evaluation Time",
                "line_1_lbl" : "FHE",
                "line_1_fmt" : "r-",
                "perform" : analyze_single }),

            AttrDict({ 
                "name" : "Figure 7 DS vs TxMS",
                "desc" : "Data Size vs Tx Message Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "max_sent_size",
                "y_axis_lbl" : "Max Tx Message Size (kb)",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 8 DS vs RxMS",
                "desc" : "Data Size vs Rx Message Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_server.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "max_received_size",
                "y_axis_lbl" : "Max Rx Message Size (kb)",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),

            AttrDict({ 
                "name" : "Figure 9 DS vs AEDS",
                "desc" : "Data Size vs Average Encrypted Data Size",
                "constants" : [{ "name" : "max_buf_size", "val" : 4096 }],
                "ref_csv_file" : "node_client.log",
                "x_axis" : "data_size",
                "x_axis_lbl" : "Number of Records",
                "y_axis" : "ave_enc_data_size",
                "y_axis_lbl" : "Average Encrypted Data Size (b)",
                "line_1_lbl" : "RSA",
                "line_1_fmt" : "r-",
                "line_2_lbl" : "FHE",
                "line_2_fmt" : "b-",
                "perform" : analyze_fhe_vs_rsa }),
    ]

    for a in analysis_tbl[6:]:
        a.perform(a)

    return

if __name__ == "__main__":
    analyze()

