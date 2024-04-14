#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: advanced header/payload separation 1 of 2
# Author: pzawadzki
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from bsc_byte_channel import bsc_byte_channel  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from msg_pdu_gen import msg_pdu_gen  # grc-generated hier_block
from msg_pdu_print import msg_pdu_print  # grc-generated hier_block
from msg_pdu_print_as_error import msg_pdu_print_as_error  # grc-generated hier_block



class npkt_05(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "advanced header/payload separation 1 of 2", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("advanced header/payload separation 1 of 2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "npkt_05")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.num_key = num_key = "packet_num"
        self.len_key = len_key = "packet_len"
        self.k = k = 7
        self.tx_format_obj = tx_format_obj = digital.header_format_crc(len_key,num_key)
        self.rx_format_crc_obj = rx_format_crc_obj = digital.header_format_crc(len_key,num_key)
        self.fs = fs = 1000000/8
        self.frame_key = frame_key = len_key
        self.fec_encoder_obj = fec_encoder_obj = fec.cc_encoder_make(8000,k, rate, polys, 0, fec.CC_TRUNCATED, True)
        self.fec_decoder_obj = fec_decoder_obj = fec.cc_decoder.make(8000,k, rate, polys, 0, (-1), fec.CC_TRUNCATED, True)
        self.Length_tag_key = Length_tag_key = "packet_len"

        ##################################################
        # Blocks
        ##################################################

        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.float_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, len_key)
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, len_key)
        self.msg_pdu_print_as_error_0 = msg_pdu_print_as_error()
        self.msg_pdu_print_0 = msg_pdu_print()
        self.msg_pdu_gen_0 = msg_pdu_gen()

        self.top_layout.addWidget(self.msg_pdu_gen_0)
        self.fec_async_encoder_0 = fec.async_encoder(fec_encoder_obj, True, True, True, 1500)
        self.fec_async_decoder_0 = fec.async_decoder(fec_decoder_obj, True, True, 1500)
        self.digital_protocol_parser_b_0_0 = digital.protocol_parser_b(rx_format_crc_obj)
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(tx_format_obj)
        self.digital_map_bb_0 = digital.map_bb([-1,1])
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            tx_format_obj.header_nbits(),
            1,
            0,
            frame_key,
            len_key,
            True,
            gr.sizeof_char,
            '',
            int(fs),
            (),
            0)
        self.digital_crc_check_0 = digital.crc_check(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, True, 0)
        self.digital_crc_append_0 = digital.crc_append(32, 0x4C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, True, True, False, 0)
        self.bsc_byte_channel_0 = bsc_byte_channel(
            BER=0,
            len_key=len_key,
        )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, fs, True, 0 if "items" == "auto" else max( int(float(fs) * fs) if "items" == "time" else int(fs), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, len_key, 0)
        self.blocks_repack_bits_bb_0_1_0 = blocks.repack_bits_bb(8, 1, len_key, False, gr.GR_LSB_FIRST)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc_append_0, 'out'), (self.fec_async_encoder_0, 'in'))
        self.msg_connect((self.digital_crc_check_0, 'ok'), (self.msg_pdu_print_0, 'pdus_in'))
        self.msg_connect((self.digital_crc_check_0, 'fail'), (self.msg_pdu_print_as_error_0, 'pdus_in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.pdu_pdu_to_tagged_stream_0_0_0, 'pdus'))
        self.msg_connect((self.digital_protocol_parser_b_0_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))
        self.msg_connect((self.fec_async_decoder_0, 'out'), (self.digital_crc_check_0, 'in'))
        self.msg_connect((self.fec_async_encoder_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.msg_pdu_gen_0, 'pdus_out'), (self.digital_crc_append_0, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.fec_async_decoder_0, 'in'))
        self.connect((self.blocks_char_to_float_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.bsc_byte_channel_0, 0))
        self.connect((self.bsc_byte_channel_0, 0), (self.blocks_repack_bits_bb_0_1_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_map_bb_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_protocol_parser_b_0_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "npkt_05")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_num_key(self):
        return self.num_key

    def set_num_key(self, num_key):
        self.num_key = num_key
        self.set_rx_format_crc_obj(digital.header_format_crc(self.len_key,self.num_key))
        self.set_tx_format_obj(digital.header_format_crc(self.len_key,self.num_key))

    def get_len_key(self):
        return self.len_key

    def set_len_key(self, len_key):
        self.len_key = len_key
        self.set_frame_key(self.len_key)
        self.set_rx_format_crc_obj(digital.header_format_crc(self.len_key,self.num_key))
        self.set_tx_format_obj(digital.header_format_crc(self.len_key,self.num_key))
        self.bsc_byte_channel_0.set_len_key(self.len_key)

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_tx_format_obj(self):
        return self.tx_format_obj

    def set_tx_format_obj(self, tx_format_obj):
        self.tx_format_obj = tx_format_obj

    def get_rx_format_crc_obj(self):
        return self.rx_format_crc_obj

    def set_rx_format_crc_obj(self, rx_format_crc_obj):
        self.rx_format_crc_obj = rx_format_crc_obj

    def get_fs(self):
        return self.fs

    def set_fs(self, fs):
        self.fs = fs
        self.blocks_throttle2_0.set_sample_rate(self.fs)

    def get_frame_key(self):
        return self.frame_key

    def set_frame_key(self, frame_key):
        self.frame_key = frame_key

    def get_fec_encoder_obj(self):
        return self.fec_encoder_obj

    def set_fec_encoder_obj(self, fec_encoder_obj):
        self.fec_encoder_obj = fec_encoder_obj

    def get_fec_decoder_obj(self):
        return self.fec_decoder_obj

    def set_fec_decoder_obj(self, fec_decoder_obj):
        self.fec_decoder_obj = fec_decoder_obj

    def get_Length_tag_key(self):
        return self.Length_tag_key

    def set_Length_tag_key(self, Length_tag_key):
        self.Length_tag_key = Length_tag_key




def main(top_block_cls=npkt_05, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
