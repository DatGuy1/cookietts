import tensorflow as tf
from text.symbols import symbols


def create_hparams(hparams_string=None, verbose=False):
    """Create model hyperparameters. Parse nondefault from given string."""

    hparams = tf.contrib.training.HParams(
        ################################
        # Experiment Parameters        #
        ################################
        epochs=1000,
        iters_per_checkpoint=1000,
        seed=1234,
        dynamic_loss_scaling=True,
        fp16_run=False,
        distributed_run=False,
        dist_backend="nccl",
        dist_url="tcp://127.0.0.1:54321",
        cudnn_enabled=True,
        cudnn_benchmark=False,
        ignore_layers=["decoder.attention_layer.F.2.weight", "decoder.attention_layer.F.2.bias","decoder.attention_layer.F.0.linear_layer.weight","decoder.attention_layer.F.0.linear_layer.bias"],
        
        ################################
        # Data Parameters              #
        ################################
        load_mel_from_disk=True,
        training_files='/media/cookie/Samsung 860 QVO/ClipperDatasetV2/filelists/mel_train_taca2_merged.txt',
        validation_files='/media/cookie/Samsung 860 QVO/ClipperDatasetV2/filelists/mel_validation_taca2_merged.txt',
        text_cleaners=['english_cleaners'],
        
        ################################
        # Audio Parameters             #
        ################################
        max_wav_value=32768.0,
        sampling_rate=48000,
        filter_length=2400,
        hop_length=600,
        win_length=2400,
        n_mel_channels=160,
        mel_fmin=50.0,
        mel_fmax=16000.0,
        
        ################################
        # Model Parameters             #
        ################################
        n_symbols=len(symbols),
        symbols_embedding_dim=512,
        
        # Encoder parameters
        encoder_kernel_size=5,
        encoder_n_convolutions=3,
        encoder_embedding_dim=512,
        
        # Decoder parameters
        n_frames_per_step=1,    # currently only 1 is supported
        decoder_rnn_dim=1024,   # 1024 original
        extra_projection=False, # another linear between decoder_rnn and the linear projection layer (hopefully helps with high sampling rates and hopefully doesn't help decoder_rnn overfit)
        prenet_dim=256,         # 256 original
        prenet_layers=2,        # 2 original
        p_prenet_dropout=0.5,   # 0.5 original
        max_decoder_steps=3500,
        gate_threshold=0.5,
        AttRNN_extra_decoder_input=False,# False original
        p_AttRNN_hidden_dropout=0.1,     # 0.1 original
        p_AttRNN_cell_dropout=0.0,       # 0.0 original
        p_DecRNN_hidden_dropout=0.1,     # 0.1 original
        p_DecRNN_cell_dropout=0.0,       # 0.0 original
        p_teacher_forcing=1.00,    # 1.00 original
        teacher_force_till=20,     # int, number of starting frames with teacher_forcing at 100%, helps with clips that have challenging starting conditions i.e breathing before the text begins.
        val_p_teacher_forcing=0.80,
        val_teacher_force_till=20,
        
        # Attention parameters
        attention_type=0,
        # 0 -> Location-Based Attention (Vanilla Tacotron2)
        # 1 -> GMMAttention (Multiheaded Long-form Synthesis)
        attention_rnn_dim=1024, # 1024 original
        attention_dim=128,      # 128 Layer original
        
        # Attention Type 0 Parameters
        attention_location_n_filters=32,   # 32 original
        attention_location_kernel_size=31, # 31 original
        
        # Attention Type 1 Parameters
        num_att_mixtures=5, # 5 original
        attention_layers=2, # 1 original
        normalize_attention_input=False, # False original
        normalize_AttRNN_output=True,    # True original
        
        # Mel-post processing network parameters
        postnet_embedding_dim=512,
        postnet_kernel_size=5,
        postnet_n_convolutions=5,
        
        # Speaker embedding
        n_speakers=512,
        speaker_embedding_dim=384, # speaker embedding size # 128 original
        
        # Reference encoder
        with_gst=True,
        ref_enc_filters=[32, 32, 64, 64, 128, 128],
        ref_enc_size=[3, 3],
        ref_enc_strides=[2, 2],
        ref_enc_pad=[1, 1],
        ref_enc_gru_size=128,
        
        # Style Token Layer
        token_embedding_size=256, # token embedding size
        token_num=10,
        num_heads=8,
        
        ################################
        # Optimization Hyperparameters #
        ################################
        use_saved_learning_rate=False,
        learning_rate=0.1e-5,
        weight_decay=1e-6,
        grad_clip_thresh=1.2,
        batch_size=64, # 32*3 = 0.377 val loss, # 2 = 0.71 val loss
        val_batch_size=64, # for more precise comparisons between models, constant batch_size is useful
        mask_padding=True,  # set model's padded outputs to padded values
        
        ##################################
        # MMI options                    #
        ##################################
        drop_frame_rate=0.00,
        use_mmi=False,
        use_gaf=True,
        max_gaf=0.01,
        global_mean_npy='global_mean.npy'
    )

    if hparams_string:
        tf.compat.v1.logging.info('Parsing command line hparams: %s', hparams_string)
        hparams.parse(hparams_string)

    if verbose:
        tf.compat.v1.logging.info('Final parsed hparams: %s', hparams.values())

    return hparams